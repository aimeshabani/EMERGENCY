

import unittest

import threading
import os
import json
import ijson    #    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   pip install ijson
import time
import pickle
import uuid
import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Dict, List
import pathlib
import traceback

# Directory setup
if not os.path.isdir(".SERVER/"):
    os.mkdir(".SERVER")

os.chdir(".SERVER")

for directory in ["REMINDERS", "DISABLED", "HISTORY", "people","ACCOUNTS"]:
    if not os.path.isdir(directory):
        os.mkdir(directory)

for history_file in ["DAY.json", "MONTH.json", "SYEAR.json","WYEAR.json"]:
    if not os.path.isfile(f"HISTORY/{history_file}"):
        json.dump({}, open(f"HISTORY/{history_file}", "w"))

# Load data
def load_data(file: str, default: Dict) -> Dict:
    try:
        return pickle.load(open(file, "rb"))
    except:
        return default

offline_messages = load_data("offline_messages", {})
locations = load_data("locations", {})
temporary = load_data("temporary", {})
confirmed = load_data("confirmed", {})
SAVE = load_data("SAVE", {})
TOUS = [] if not os.path.isfile("TOUS") else pickle.load(open("TOUS","rb"))



HOST = "0.0.0.0"
PORT = 8080

# Dictionaries to store client data
connected_clients: Dict[str, StreamWriter] = {}

def READER(path,ext,recipients):
    if ext==".bin":
        data=pickle.load(open(path,"rb"))
    else:
        data=json.load(open(path,"r"))

    M={"data":data,"deliver":data["sidd"],"recipients":[recipients],"action":"src"}


    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(Store(M))
    loop.close()

def instancer(key,path,adress,receipient):
    """
    FIND IN ACCOUNTS/BUSY    idd[:8]        not history
    THEN
    ACCOUNTS_CHATS/CITY    CHATS             to save MB
    """
    global goten
    def search_in_json(file_path, target_word):
        with open(file_path, 'r') as file:
            parser = ijson.parse(file)  # Incremental JSON parsing to save memory
            for prefix, event, value in parser:
                if isinstance(value, str) and target_word in value:
                    return True
        return False

    def search_in_binary(file_path, target_word):
        with open(file_path, 'rb') as file:
            chunk_size = 1024  # Read in small chunks (1 KB)
            while chunk := file.read(chunk_size):
                # Decode binary to string with error handling
                try:
                    if target_word in chunk.decode(errors='ignore'):
                        return True
                except UnicodeDecodeError:
                    continue  # Ignore decoding errors for binary data
        return False

    def search_word_in_files(start_directory, target_word,receipient):
        global goten
        for root, dirs, files in os.walk(start_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_name.endswith('.json'):
                    if file_name != "history.json":
                        if search_in_json(file_path, target_word):
                            threading.Thread(target=READER,args=(file_path,receipient,".json") ).start()
                            goten+=1
                else:
                    # Assuming all other files are binary
                    if search_in_binary(file_path, target_word):
                        threading.Thread(target=READER,args=(file_path,receipient,".bin") ).start()
                        goten += 1
        return True

    goten=0

    for x in path :
        if search_word_in_files("ACCOUNTS/"+x, key,receipient) :
            print("got something there")

    if search_word_in_files("ACCOUNTS_CHATS/"+adress[0]+"/"+adress[1], key,receipient):
        print("got something there")
    if goten < 3 :
        search_word_in_files("ACCOUNTS_CHATS/"+adress[0], key,receipient) #  pay

async def histO(data):
    # "path":[time.strftime("%Y"),time.strftime("%B"),time.strftime("%d"),time.strftime("%H:%M:%S")]
    Y = json.load(open("HISTORY/" + data["st"], "r"))
    if not Y.get(data["path"][0], 0):
        Y[data["path"][0]] = {"TOTAL": "0"}
    if not Y[data["path"][0]].get(data["path"][1], 0):
        Y[data["path"][0]][data["path"][1]] = {"TOTAL": "0"}
    if not Y[data["path"][0]][data["path"][1]].get(data["path"][2], 0):
        Y[data["path"][0]][data["path"][1]][data["path"][2]] = {"TOTAL": "0"}
    # if not Y[data["path"][0]][data["path"][1]][data["path"][3]].get(data["path"][3], 0):
    #     Y[data["path"][0]][data["path"][1]][data["path"][2]][data["path"][3]] = {"TOTAL": "0"}

    TD = float(Y[data["path"][0]][data["path"][1]][data["path"][2]]["TOTAL"]) + float(data["sum"])
    TM = float(Y[data["path"][0]][data["path"][1]]["TOTAL"]) + float(data["sum"])
    TY = float(Y[data["path"][0]]["TOTAL"]) + float(data["sum"])

    Y[data["path"][0]][data["path"][1]][data["path"][2]][data["path"][3]] = float(data["sum"])
    Y[data["path"][0]][data["path"][1]][data["path"][2]]["TOTAL"] = TD
    Y[data["path"][0]][data["path"][1]]["TOTAL"] = TM
    Y[data["path"][0]]["TOTAL"] = TY

    json.dump(Y, open("HISTORY/" + data["st"], "w"))

def ftp():
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
    direct=os.getcwd()
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user("aime shabani", "12435687", direct, perm='elradfmwMT')  #  "/"

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    handler.masquerade_address = '195.35.23.244'
    handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    server = FTPServer(("0.0.0.0", 2121), handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5
    print('Ftp Server running on http://0.0.0.0:2121')
    # Start the FTP server
    server.serve_forever()

async def cred_name(idd: str, t: str, writer: StreamWriter):

    if idd+'.json' in os.listdir("people/"):
        retrn = json.load(open("people/" + idd + '.json', "r"))
        ux = ""
        for user in retrn.keys():
            names = user[user.index("_") + 1:].replace("@", " ")

            if names == t or t.split(" ")[0] == names.split(" ")[0] or t.split(" ")[-1] == names.split(" ")[-1] or t.split(" ")[0].lower() == names.split(" ")[0].lower() or t.split(" ")[-1].lower() == names.split(" ")[1].lower() or t.title() == names.title() or t.split(" ")[0].title() == names.split(" ")[0].title() or t.split(" ")[-1].title() == names.split(" ")[-1].title():
                ux = user

        if ux != "":
            found = {"status": "exist", "recipients":[retrn[ux]["idd"]],"action": "rsp_login", "pwd": retrn[ux]["pwd"]}
        else:
            found = {"status": "create_account", "recipients":[retrn[ux]["idd"]],"action": "rsp_login"}
        print("found in cred_name")

        await keep(found)
        # msg = json.dumps(found)
        # writer.write(msg.encode())
        # await writer.drain()
        if found["status"] == "exist":
            open("people/shabani", "a").write(time.strftime("%d %B %Y %H:%M:%S") + "  " + t + "  " + idd + "  Logged in\n")
    else:
        print("No account for this Organization")
        # json.dump({}, open("people/" + idd + ".json", "w"))
        # found = {"status": "create_account", "action": "rsp_login","recipients":[retrn[ux]["idd"]]}
        # msg = json.dumps(found)
        # writer.write(msg.encode())
        # await writer.drain()

async def cred_pwd(M, writer: StreamWriter):
    open("logs", "a").write(json.dumps(M))
    sv = {"action": "ALL", "DATA": SAVE}
    writer.write(json.dumps(sv).encode("utf-8"))
    await writer.drain()

async def NEW_AC(dicti):
    """clients number
        active
        men number
        WOMEN NUMBER
        younger
        older
        common deposit
        common erea"""
    if not os.path.isdir("temp"):
        os.mkdir("temp")

    json.dump(dicti["acc"], open("temp/" + dicti["acc"]["idd"] + ".json", "w"))

    all = json.load(open("people/" + dicti["idd"] + ".json", "r"))
    all[dicti["acc"]["idd"] + "_" + dicti["acc"]["Name"][0] + "@" + dicti["acc"]["Name"][1]] = dicti["acc"]
    json.dump(all, open("people/" + dicti["idd"] + ".json", "w"))

async def NEW_CL(M):
    if not os.path.isdir("C_TEMPS"):
        os.mkdir("C_TEMPS")
    if not os.path.isdir("CLIENTS"):
        os.mkdir("CLIENTS")
    if not os.path.isdir("C_IMG"):
        os.mkdir("C_IMG")
    if not os.path.isfile("CLIENTS/" + M["idd"] + ".json"):
        json.dump({}, open("CLIENTS/" + M["idd"] + ".json", "w"))

    json.dump(M["acc"], open("C_TEMPS/" + M["acc"]["idd"] + ".json", "w"))

    all = json.load(open("CLIENTS/" + M["idd"] + ".json", "r"))
    all[M["acc"]["idd"] + "_" + M["acc"]["Name"] + "@" + M["acc"]["Post_Name"]] = M["acc"]
    json.dump(all, open("CLIENTS/" + M["idd"] + ".json", "w"))
    print("New account made")

    if not os.path.isdir("DATA"):
        os.mkdir("DATA")
    if not os.path.isfile("DATA/analysis"):
        dt = {"cl_N": 0, "men": 0, "women": 0, "older": [], "younger": [], "high_dep": [], "low_dep": [],
              "high_actv": [], "low_actv": [], "com_erea": ""}
        pickle.dump(dt, open("DATA/analysis", "wb"))
    data = pickle.load(open("DATA/analysis", "rb"))

    cn = data["cl_N"] + 1
    if dicti["acc"]["Gender"] == "Male":
        male = data["men"] + 1
        data["men"] = male
    else:
        male = data["women"] + 1
        data["women"] = male
    data["cl_N"] = cn
    lst = {}
    area = {}
    for x in all.keys():
        list[int(all[x]["Birth year"])] = x
        if not area.get(all[x]["Country/district/city"], 0):
            area[all[x]["Country/district/city"]] = [x]
        else:
            area[all[x]["Country/district/city"]].append(x)

    old = min(lst.keys())
    youn = max(lst.keys())
    data["younger"] = [youn, lst[youn]]
    data["older"] = [old, lst[old]]
    x = 0
    cmer = ''
    for k in area.keys():
        if len(area[k]) > x:
            x = len(k)
            cmer = k
    data["com_erea"] = cmer

    pickle.dump(data, open("DATA/analysis", "wb"))
    data["recipients"] = TOUS
    data["action"] = "Activity"

    await TRANSACTION(data)
    # await keep(data)

    del area
    del lst
    del all
    del data
    del old
    del cmer
    del youn
    del x
    del male
    del cn

    # {"cl_N":0,"men":0,"women":0,"older":[],"younger":[],"high_dep":[],"low_dep":[],"high_actv":[],"low_actv":[],"com_erea":""}
    # pickle.dump(data, open("DATA/analysis", "wb"))
    # data=pickle.load(open("DATA/analysis","rb"))
    # data["recipients"]=TOUS
    # data["action"]="Activity"

async def keep(M):
    return
    # print("in keep() ",M)
    if "str" in str(type(M)):
        if len(M) < 2:
            return
        else:
            try:
                M = json.loads(M)
            except:
                return
    elif M.get("action") in ["location", "Received", "search", "deliver", 'UPDATES']:
        return
    elif not M.get("deliver"):
        M["deliver"] = str(uuid.uuid4())[:12]
    if isinstance(M, dict) and M != {}:
        for rec in M.get("recipients", []):
            if not temporary.get(rec):
                if not connected_clients.get(rec):
                    if not rec in offline_messages.keys():
                        offline_messages[rec] = []
                    offline_messages[rec].append(json.dumps(M))
                else:
                    temporary[rec] = [[connected_clients[rec], json.dumps(M)]]
            else:
                if not connected_clients.get(rec):
                    if not rec in offline_messages.keys():
                        offline_messages[rec] = []
                    offline_messages[rec].append(json.dumps(M))
                else:
                    temporary[rec].append([connected_clients[rec], json.dumps(M)])

async def Store(M):
    print("____"*1000,M)

    if M.get("data",0):
        if not os.path.exists("Temp_Emerg/"):
            os.makedirs("Temp_Emerg/" )
            json.dump(M, open("Temp_Emerg/"+M["data"].get("sidd", 0) + ".json", "w"))
        else:
            json.dump(M, open("Temp_Emerg/" + M["data"].get("sidd", 0) + ".json", "w"))

        if connected_clients.get(M["recipients"][0],0):
            sms=json.dumps(M)
            Writer=connected_clients[M["recipients"][0]]
            Writer.write(sms.encode())
            await Writer.drain()
            print(M["data"]["sidd"] , "is sent1")
    else:
        if not os.path.exists("Temp_Emerg/"):
            os.makedirs("Temp_Emerg/")
            json.dump(M, open("Temp_Emerg/" + M.get("sidd", 0) + ".json", "w"))
        else:
            json.dump(M, open("Temp_Emerg/" + M.get("sidd", 0) + ".json", "w"))

        if connected_clients.get(M["recipients"][0], 0):
            sms = json.dumps(M)
            Writer = connected_clients[M["recipients"][0]]
            Writer.write(sms.encode())
            await Writer.drain()
            print(M["sidd"], "is sent2")

async def NEW_ALR(M):
    print(M)
    if M.get("data",0):
        json.dump(M["data"], open("REMINDERS/" + M["data"]["idd"] + "@" + M["data"]["domain"].upper() + ".json", "w"))
    else:
        json.dump(M, open("REMINDERS/" + M["idd"] + "@" + M["domain"].upper() + ".json", "w"))

async def TOKEN(M):
    toc = M["data"]["token"]
    print("token: ",toc,M)
    M = M["data"]
    for file in os.listdir("REMINDERS/"):
        print("Alarm: ",file)
        idd=file[:file.index("@")]
        if idd.endswith(toc[-3:]):      #   if file[:-5].endswith(toc[-3:]):
            if idd.startswith(toc[:3]):
                print("found: ",file)
                dic = json.load(open("REMINDERS/" + file, "r"))
                if not M["name"] in dic["Who can see"] :
                    dic["Who can see"].append(M["name"])
                if not M["name"] in dic["who can remind"]:
                    dic["who can remind"].append(M["name"])
                if not M["name"] in dic["who receive same reminder"]:
                    dic["who receive same reminder"].append(M["name"])

                # rec=dic.get("recipients",[])
                rec=TOUS
                if not M["idd"] in rec :
                    rec.append(M["idd"])
                data = {"recipients":rec,"idd":dic["idd"],"action":"New Alarm","action2":"token","data":dic}
                print(data)
                await keep(data)
                json.dump(dic, open("REMINDERS/" + file, "w"))

async def All_c(M, writer: StreamWriter):
    cli = json.load(open("CLIENTS/" + M["idd"] + ".json", "r"))
    cli["action"] = "All_c"
    all = json.dumps(cli)
    writer.write(all.encode())
    await writer.drain()

async def search2(M, writer: StreamWriter):
    exc = ["history", "Password", "photo", "$"]
    got = []
    for x in os.listdir("C_TEMPS/"):
        dic = json.load(open("C_TEMPS/" + x, "r"))
        for i in dic.keys():
            if not i in exc:
                if dic[i].strip().lower() == M["kw"].strip().lower() or M["kw"].strip().lower() in dic[i].strip().lower() or dic[i].strip().lower() in M["kw"].strip().lower():
                    got.append(dic)
                    print("got :  ", dic)
    await keep({"action": "s_r", "sender": M["sender"], "recipients": M["recipients"], "data": got})
    print("All found : ", len(got))

async def search(M, writer: StreamWriter):
    exc = ["history", "Password", "photo", "$"]
    got = []
    for x in os.listdir("C_TEMPS/"):
        dic = json.load(open("C_TEMPS/" + x, "r"))   #dicti["acc"]["idd"] + "_" + dicti["acc"]["Name"][0] + "@" + dicti["acc"]["Name"][1]]
        for i in dic.keys():
            if not i in exc:
                if dic[i].strip().lower() == M["kw"].strip().lower() or M["kw"].strip().lower() in dic[i].strip().lower() or dic[i].strip().lower() in M["kw"].strip().lower():
                    got.append(dic["idd"])
                    print(dic)
                    await keep({"action": "s_r", "sender": M["sender"], "recipients": M["recipients"], "data": {"acc":x[:-5]+"_" + dic["Name"] + "@" + dic["Post_Name"],"idd":dic["idd"],"keyw":i+"@"+dic[i]+"$"+M["kw"]}})
                    print("got :  ", dic)
    await keep({"recipients": M["recipients"], "action": "s_r_e"})
    print("All found : ", got)

async def Received2(key):
    if os.path.isfile("Temp_Emerg/"+key+".json"):
        os.remove("Temp_Emerg/"+key+".json")
        print("Message ",key," deleted")
    else:
        print("THIS FILE DOES NOT EXIT: ",key+".json")

async def received(key):
    for idd in offline_messages.keys():
        for sms in offline_messages[idd]:
            if isinstance(sms, str):
                if key in sms:
                    offline_messages[idd].remove(sms)
            else:
                d = json.loads(sms)
                if d.get("deliver") == key:
                    offline_messages[idd].remove(sms)

    for idd in temporary.keys():
        for sms in temporary[idd]:
            if isinstance(sms[1], str):
                if key in sms[1]:
                    temporary[idd].remove(sms)
            else:
                d = json.loads(sms[1])
                if d.get("deliver") == key:
                    temporary[idd].remove(sms)

async def TRANSACTION(M):  #  THE RECEIPT WON'T PRINT IF THE SERVER HASN'T STORED
    if M.get("action",0) != "Activity":   # After new client, send updates.   After transaction, send updates too
        print("Transaction ",M)
        k = {"action": "55","path":M["path"]}
        if M["reason"] == "saving":
            k["st"] = "SYEAR.json"
            k["sum"]=M.get("info", "0")
            # "path":[time.strftime("%Y"),time.strftime("%B"),time.strftime("%d"),time.strftime("%H:%M:%S")]

            d = json.load(open("C_TEMPS/" + M["idd"] + ".json", "r"))
            d["$"]["principal"].append(M.get("info", "0"))
            d["history"][M["time"]] = M["info"]
            json.dump(d, open("C_TEMPS/" + M["idd"] + ".json", "w"))
            # # d = json.load(open("HISTORY/DAY.json", "r"))
            # # d[time.strftime("%H:%M:%S")] = M.get("info", "0")
            # # json.dump(d, open("HISTORY/DAY.json", "w"))
            #
            # d = json.load(open("HISTORY/MONTH.json", "r"))
            # if not d.get(time.strftime("%d")):
            #     d[time.strftime("%d")] = M.get("info", "0")
            #     k["M"]=[time.strftime("%d"),M.get("info", "0")]
            # else:
            #     value = float(d[time.strftime("%d")]) + float(M.get("info", "0"))
            #     d[time.strftime("%d")] =str(value)
            #     k["M"] = [time.strftime("%d"),str(value)]
            # json.dump(d, open("HISTORY/MONTH.json", "w"))
            #
            # d = json.load(open("HISTORY/YEAR.json", "r"))
            # if not d.get("Y"):
            #     d["Y"]={}
            # if not k.get("Y"):
            #     k["Y"]={}
            # if not k["Y"].get(time.strftime("%Y"),0):
            #     k["Y"][time.strftime("%Y")]={}
            #
            # if not d["Y"].get(time.strftime("%Y")):
            #     d["Y"][time.strftime("%Y")]={time.strftime("%B"):M.get("info", "0")}
            #     # d[time.strftime("%Y")] = M.get("info", "0")
            #     k["Y"][time.strftime("%Y")][time.strftime("%B")]= M.get("info", "0")
            # else:
            #     value = float(d["Y"][time.strftime("%Y")][time.strftime("%B")]) + float(M.get("info", "0"))
            #     d["Y"][time.strftime("%Y")][time.strftime("%B")] =str(value)
            #     k["Y"][time.strftime("%Y")][time.strftime("%B")] = str(value)
            # json.dump(d, open("HISTORY/YEAR.json", "w"))
            print("Done saving")
            del d

        elif M["reason"] == "withdraw":
            k["st"] = "WYEAR.json"
            k["sum"] =  M.get("info", "0")
            # "path":[time.strftime("%Y"),time.strftime("%B"),time.strftime("%d"),time.strftime("%H:%M:%S")]

            d = json.load(open("C_TEMPS/" + M["idd"] + ".json", "r"))
            d["$"]["principal"].append("-" + M.get("info", "0"))
            d["history"][M["time"]] = "-" + M["info"]
            json.dump(d, open("C_TEMPS/" + M["idd"] + ".json", "w"))

            # d = json.load(open("HISTORY/DAY.json", "r"))
            # d[time.strftime("%H:%M:S")] = "-" + M.get("info", "0")
            # json.dump(d, open("HISTORY/DAY.json", "w"))
            #
            # d = json.load(open("HISTORY/MONTH.json", "r"))
            # if not d.get(time.strftime("%d")):
            #     d[time.strftime("%d")] = "-" + M.get("info", "0")
            #     k["M"] = [time.strftime("%d"),  "-" + M.get("info", "0")]
            # else:
            #     value = float(d[time.strftime("%d")]) - float(M.get("info", "0"))
            #     d[time.strftime("%d")] = str(value)
            #     k["M"] = [time.strftime("%d"),  "-" + str(value)]
            # json.dump(d, open("HISTORY/MONTH.json", "w"))
            #
            # d = json.load(open("HISTORY/YEAR.json", "r"))
            # if not d.get(time.strftime("%B")):
            #     d[time.strftime("%B")] = "-" + M.get("info", "0")
            #     k["Y"] = [time.strftime("%B"), "-" + M.get("info", "0")]
            # else:
            #     value = float(d[time.strftime("%B")]) - float(M.get("info", "0"))
            #     d[time.strftime("%B")] =  str(value)
            #     k["Y"] = [time.strftime("%B"), "-" + str(value)]
            # json.dump(d, open("HISTORY/YEAR.json", "w"))

            print("Done withdraw")
            del d
        elif M["reason"] == "activity":
            d = json.load(open("C_TEMPS/" + M["idd"] + ".json", "r"))
            d["activity"] = "0" if d.get("activity") == "1" else "1"
            json.dump(d, open("C_TEMPS/" + M["idd"] + ".json", "w"))
            print("No interest generation to", d["Name"])
            del d

        elif M["reason"] == "disable":
            d = json.load(open("C_TEMPS/" + M["idd"] + ".json", "r"))
            json.dump(d, open("DISABLED/" + M["idd"] + ".json", "w"))
            os.remove("C_TEMPS/" + M["idd"] + ".json")
            print(d["Name"], "disabled")
            del d

        k["recipients"]=TOUS
        await keep(k)
        await histO(k)

    lw_act=[1000000000,"x"]
    h_act=[0,"x"]
    l_dp=[100000000000,"x"]
    h_dp=[0,"x"]

    for x in os.listdir("C_TEMPS/"):
        dc=json.load(open("C_TEMPS/"+x))
        if len(dc["$"]["principal"]) < lw_act[0] :
            lw_act=[len(dc["$"]["principal"]),dc["photo"]]

        if len(dc["$"]["principal"]) > h_act[0] :
            h_act=[len(dc["$"]["principal"]),dc["photo"]]

        if eval("+".join(dc["$"]["principal"])) < l_dp[0] :
            l_dp=[eval("+".join(dc["$"]["principal"])),dc["photo"]]

        if eval("+".join(dc["$"]["principal"])) > h_dp[0] :
            h_dp=[eval("+".join(dc["$"]["principal"])),dc["photo"]]
    try:
        del dc
    except:
        pass

    data = pickle.load(open("DATA/analysis", "rb"))
    data["high_dep"]=h_dp
    data["low_dep"]=l_dp
    data["high_actv"]=h_act
    data["low_actv"]=lw_act

    pickle.dump(data, open("DATA/analysis", "wb"))
    data["recipients"]=TOUS
    data["action"]="Activity"
    await keep(data)
    del data
    del h_dp
    del l_dp
    del h_act
    del lw_act
    # {"cl_N":0,"men":0,"women":0,"older":[],"younger":[],"high_dep":[],"low_dep":[],"high_actv":[],"low_actv":[],"com_erea":""}

    try:
        del k
    except Exception as e:
        print("TRANSACTION: ",e)
        pass

async def UPDATES(M):
    D = {"recipients": M["recipients"], "action": "UPDATES2", "tp": "DAY", "data1": json.load(open("HISTORY/DAY.json", "r"))}
    await keep(D)

    MN = {"recipients": M["recipients"], "action": "UPDATES2", "tp": "MONTH", "data1": json.load(open("HISTORY/MONTH.json", "r"))}
    await keep(MN)

    Y = {"recipients": M["recipients"], "action": "UPDATES2", "tp": "YEAR", "data1": json.load(open("HISTORY/YEAR.json", "r"))}
    await keep(Y)

async def ONE(M, writer):
    print("M ",M)
    try:
        k = {"deliver":str(uuid.uuid4())[:12],"data": json.load(open("C_TEMPS/" + M["one"] + ".json")), "recipients": M["recipients"], "action": M["action"]}
    except Exception as e :
        print("k ",e)
    try:
        writer.write(  json.dumps(k).encode()  )
        await writer.drain()
        del k

    except:
        await keep(k)
        del k

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^               EMERGENCY        ^^^^^^^^^^^^^^^^^^^^
async def N_USER(M):

    """
    REPLACE NAMES,ADRESS IN ME.JSON
    MOVE DATA FROM WORLD/EVERYWHERE  TO ME[ADRESS]
    """
    if not os.path.exists("ACCOUNTS_CHATS/"+M["data"]["adress"][0]):     #  "ACCOUNTS/"+M["idd"]+"Items"
        os.makedirs("ACCOUNTS_CHATS/"+M["data"]["adress"][0])

    if not os.path.exists("ACCOUNTS_CHATS/"+M["data"]["adress"][0]):     #  "ACCOUNTS/"+M["idd"]+"Items"
        os.mkdir("ACCOUNTS_CHATS/"+M["data"]["adress"][0])

    if not os.path.exists("ACCOUNTS_CHATS/"+M["data"]["adress"][0]+"/"+M["data"]["adress"][1]):     #  "ACCOUNTS/"+M["idd"]+"Items"
        os.mkdir("ACCOUNTS_CHATS/"+M["data"]["adress"][0]+"/"+M["data"]["adress"][1])

    if not os.path.exists("COUNTRIES/"+M["data"]["adress"][0]+"/"+M["data"]["adress"][1]):     #  "ACCOUNTS/"+M["idd"]+"Items"
        os.makedirs("COUNTRIES/"+M["data"]["adress"][0]+"/"+M["data"]["adress"][1])

    if not os.path.exists("ACCOUNTS/"+M["data"]["idd"]):     #  "ACCOUNTS/"+M["idd"]+"Items"
        os.mkdir("ACCOUNTS/"+M["data"]["idd"])

    if not os.path.exists("ACCOUNTS/"+M["data"]["idd"]+"/web/"):     #  "ACCOUNTS/"+M["idd"]+"Items"
        os.mkdir("ACCOUNTS/"+M["data"]["idd"]+"/web/")

    if not os.path.exists("ACCOUNTS/"+M["data"]["idd"]+"/Items/"):     #  "ACCOUNTS/"+M["idd"]+"Items"
        os.mkdir("ACCOUNTS/"+M["data"]["idd"]+"/Items/")

    if not os.path.isfile("ACCOUNTS/" + M["data"]["idd"] + "/history.json"):
        json.dump({}, open("ACCOUNTS/" + M["data"]["idd"] + "/history.json", "w"))   #   SCROLL    NEXT

    json.dump(M["data"],open("ACCOUNTS/"+M["data"]["idd"]+"/"+M["data"]["idd"]+".json","w"))
    json.dump(M["data"], open("COUNTRIES/" + M["data"]["adress"][0]+"/"+M["data"]["adress"][1]+"/"+ M["data"]["idd"] + ".json", "w"))

    # us={"action":"wlcm","idd":M["data"]["idd"],"catch_word":M.get("C_W","Hi")}
    # zone = await _files(dir="COUNTRIES/" + M["data"]["adress"][0] + "/" + M["data"]["adress"][1])
    # for idd in zone:  # if M[recipients]=zone        the message will be 32MB  to 1000,000 users
    #     us["recipients"] = [idd.replace(".json", "").replace(".bin", "")]
        # await Store(us)

async def B_U(M):
    print(M)
    try:
        shop=json.load(open("ACCOUNTS/"+M["data"]["idd"]+"/"+M["data"]["idd"][:8]+".json","r"))
        BS=shop["BUSY"]+M["data"]["BUSY"]
        PHT=shop["pht"]+M["data"]["pht"]
        shop["BUSY"]=BS
        shop["pht"]=PHT
        json.dump(shop,open("ACCOUNTS/"+M["data"]["idd"]+"/"+M["data"]["idd"][:8]+".json", "w"))

        if not os.path.exists("ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"]):  # zone[0] =N       zone:Ntungamo            #  "/"+M["data"]["zone"][1]+
            os.makedirs("ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin", "").replace(".json",
                                                                                                               ""))  # "/"+M["data"]["zone"][1] +
        json.dump(M["data"], open("ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin", "").replace(".json", "") + ".json","w"))

        del shop
        del BS
        del PHT
    except:
        json.dump(M["data"], open("ACCOUNTS/"+M["data"]["idd"]+"/"+M["data"]["idd"][:8]+".json", "w"))
    if len( M["data"]["BUSY"])<=3:
        zone = await _files(dir="COUNTRIES/" + M["data"]["zone"][0] + "/" + M["data"]["zone"][1])
        for idd in zone:  # if M[recipients]=zone        the message will be 32MB  to 1000,000 users
            M["recipients"] = [idd.replace(".json", "").replace(".bin", "")]
            await Store(M)

async def Filt(fls,his):
    print("fls:", fls, " his: ", his)
    fls=[x for x in fls if ".json" in x]
    for i in fls:  # his["ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]]:
        try:
            if i in his :
                fls.remove(i)  # his["ACCOUNTS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"]]
        except:
            pass  # fls.remove(i for i in his["ACCOUNTS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]])

    try:  # the list might be empty
        rest = fls[0].replace(".json", "") + ".json"
    except:
        rest = ""
    print("fls:",fls," his: ",his)
    return rest

async def ACTIVITY(M):
    # print(M["data"]["schm"])
    try:
        if M["action"] in ["inbx","cht"]:
            await Store(M)
            if not os.path.exists("ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"] ):    #zone[0] =N       zone:Ntungamo            #  "/"+M["data"]["zone"][1]+
                os.makedirs("ACCOUNTS_CHATS/"+M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin","").replace(".json","")  )   # "/"+M["data"]["zone"][1] +
            json.dump(M["data"], open("ACCOUNTS_CHATS/"+M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin","").replace(".json","") + ".json", "w"))

        elif M["action"]== "zone" :
            if M["data"].get("tg",0) :
                print("tg ",M)
                if not os.path.exists("ACCOUNTS_CHATS/"+M["data"]["zone"][0] + "/" + M["data"]["schm"] ):      #zone[0] =N       zone:Ntungamo
                    os.makedirs("ACCOUNTS_CHATS/"+M["data"]["zone"][0] + "/" + M["data"]["schm"])
                zone = await _files(dir="TALENTS/" + M["data"]["zone"][0] + "/" + M["data"]["zone"][1]+"/"+ M["data"]["tg"] )
                for idd in zone:  # if M[recipients]=zone        the message will be 32MB  to 1000,000 users
                    M["recipients"] = [idd.replace(".json", "").replace(".bin", "")]
                    await Store(M)
            else:
                if not os.path.exists("ACCOUNTS_CHATS/"+M["data"]["zone"][0] + "/" + M["data"]["schm"] ):      #zone[0] =N       zone:Ntungamo
                    os.makedirs("ACCOUNTS_CHATS/"+M["data"]["zone"][0] + "/" + M["data"]["schm"])
                json.dump(M["data"], open("ACCOUNTS_CHATS/"+M["data"]["zone"][0] + "/" + M["data"]["schm"] + ".json", "w"))

                zone=await _files(dir="COUNTRIES/"+M["data"]["zone"][0] + "/" + M["data"]["zone"][1])
                for idd in zone:                          #  if M[recipients]=zone        the message will be 32MB  to 1000,000 users
                    M["recipients"]=[idd.replace(".json","").replace(".bin","")]
                    print("zone: ",M)#
                    await Store(M)

        elif M["action"] == "next":
            print("next: ",M)
            if not os.path.isfile("ACCOUNTS/"+M["data"]["idd"]+"/history.json"):
                json.dump({"ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]:[]},open("ACCOUNTS/"+M["data"]["idd"]+"/history.json","w") )

            his=json.load(open("ACCOUNTS/"+M["data"]["idd"]+"/history.json","r"))
            print("his:", his)
            if not his.get("ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"],0):
                his["ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]]=[]

            fls= await _files("ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"])


            rest=await Filt(fls,his["ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" +M["data"]["schm"]])
            if rest == "":
                return
            print("his/////////// ",his)
            if not rest in his["ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" +M["data"]["schm"]] :
                try:  #  IN CASE THE FOLDER IS EMPTY,  THE JSON.LOAD WILL CRASH
                    file=json.load(open("ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"].replace(".bin", "").replace(".json", "")+"/"+rest,"r"))
                    his["ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin", "").replace(".json", "")].append(rest)
                    json.dump(his, open("ACCOUNTS/" + M["data"]["idd"] + "/history.json", "w"))
                    file["schm"]=M["data"]["schm"].replace(".bin", "").replace(".json", "")+"/"+rest
                    M["deliver"]=file["sidd"]
                    M["data"]=file
                    await Store(M)

                except Exception as e :
                    print(f"ERROR: ==== {e}",traceback.format_exc())
                    pass

        elif M["action"] == "H_nX":
            print("H_nX: ",M)
            if not os.path.isfile("ACCOUNTS_CHATS/"+M["data"]["idd"]+"/history.json"):
                json.dump({"ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]:[]},open("ACCOUNTS/"+M["data"]["idd"]+"/history.json","w") )

            his=json.load(open("ACCOUNTS/"+M["data"]["idd"]+"/history.json","r"))
            if not his.get("ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"],[]):
                his["ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]]=[]

            fls= await _files("ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"])
            for i in his["ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]]:
                try:
                    fls.remove(i)                                                                           #   his["ACCOUNTS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"]]
                except:
                    pass                                                                                   # fls.remove(i for i in his["ACCOUNTS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]])

            try:   #       the list might be empty
                rest=fls[0].replace(".json","")+".json"
            except:
                rest=""

            his["ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" +M["data"]["schm"]].append(rest)
            json.dump(his, open("ACCOUNTS/" + M["data"]["idd"] + "/history.json", "w"))

            try:  #  IN CASE THE FOLDER IS EMPTY,  THE JSON.LOAD WILL CRASH
                file=json.load(open("ACCOUNTS_CHATS/"+M["data"]["zone"][0] +"/" + M["data"]["schm"]+"/"+rest,"r"))

                file["schm"]=M["data"]["schm"]+"/"+rest
                M["deliver"]=file["sidd"]
                M["data"]=file
                await Store(M)
            except Exception as e :
                print(">>>>>>>>> ",e)
                pass

        elif M["action"] == "contact":
            contact=json.load(open("ACCOUNTS/"+M["idd"]+"/"+M["idd"][:8]+".json","r"))
            B_U=json.load(open("ACCOUNTS/"+M["idd"]+"/"+M["idd"][:8]+".json","r"))
            M["contact"]=B_U
            await Store(M)
            del B_U

        elif M["action"] == "JB":

            if not os.path.exists("TALENTS/"+M["data"]["zn"][0]+"/"+M["data"]["zn"][1]):
                os.makedirs("TALENTS/"+M["data"]["zn"][0]+"/"+M["data"]["zn"][1])

            for tl in M["data"]["jb"]:
                if not os.path.exists("TALENTS/" + M["data"]["zn"][0] + "/" + M["data"]["zn"][1]+"/"+tl):
                    os.makedirs("TALENTS/" + M["data"]["zn"][0] + "/" + M["data"]["zn"][1]+"/"+tl)

                if not M["data"]["idd"] in os.listdir("TALENTS/"+M["data"]["zn"][0]+"/"+M["data"]["zn"][1]+"/"+tl):                           #  + M["data"]["idd"]
                    open("TALENTS/"+M["data"]["zn"][0]+"/"+M["data"]["zn"][1]+"/"+tl+"/"+M["data"]["idd"],"w").write(M["data"]["idd"])


            for tl in M["data"]["old"]:
                if tl in os.listdir("TALENTS/"+M["data"]["zn"][0]+"/"+M["data"]["zn"][1]+"/"+tl+"/"):                               #  + M["data"]["idd"]
                    os.remove("TALENTS/"+M["data"]["zn"][0]+"/"+M["data"]["zn"][1] +"/"+tl +"/"+M["data"]["idd"])

        elif M["action"] == "lk":
            if not os.path.isdir("ACCOUNTS/"+M["data"]["idd"]+"/likes"):
                os.mkdir("ACCOUNTS/" + M["data"]["idd"] + "/likes")
            if M["data"]["idd"] in await _files("ACCOUNTS/"+M["data"]["idd"]+"/likes"):
                os.remove("ACCOUNTS/"+M["data"]["idd"]+"/likes/"+M["data"]["idd"])
                dicti = json.load(open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"]+".json", "r"))
                lks = int(dicti.get("lk", "0")) - 1
                dicti["lk"] = lks
                json.dump(dicti, open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"]+".json", "w"))
            else:
                open("ACCOUNTS/"+M["data"]["idd"]+"/likes/"+M["data"]["idd"],"w").write(M["data"]["idd"])
                dicti=json.load(open("ACCOUNTS/"+M["data"]["idd"]+"/"+M["data"]["idd"]+".json", "r"))
                lks=int(   dicti.get("lk","0")   ) +1
                dicti["lk"]=lks
                json.dump(dicti,open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"]+".json", "w"))

            try:
                rson = json.load(open( "ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin", "").replace(".json", "") + ".json","r"))
                lkcs = int(rson.get("lk", "0")) + int(M["data"]["N"])
                rson["lk"] = str(lkcs)
                json.dump(rson, open( "ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin", "").replace(".json", "") + ".json","w"))
            except:
                rson = json.load(open("ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/Activities/" + M["data"]["schm"].replace(".bin", "").replace(".json", "") + ".json", "r"))
                lkcs = int(rson.get("lk", "0")) + int(M["data"]["N"])
                rson["lk"] = str(lkcs)
                json.dump(rson, open( "ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/Activities/" + M["data"]["schm"].replace(".bin", "").replace( ".json", "") + ".json", "w"))

            rson = json.load(open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"][:8] + ".json", "r"))
            lkcs = int(rson.get("lk", "0")) + int(M["data"]["N"])
            rson["lk"] = str(lkcs)
            json.dump(rson, open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"][:8] + ".json", "w"))

            del dicti
            del lks
            del lkcs
            del M

        elif M["action"] == "bl":
            if not os.path.isdir("ACCOUNTS/" + M["data"]["idd"] + "/blk"):
                os.mkdir("ACCOUNTS/" + M["data"]["idd"] + "/blk")
            if M["data"]["idd"] in await _files("ACCOUNTS/" + M["data"]["idd"] + "/blk"):
                os.remove("ACCOUNTS/" + M["data"]["idd"] + "/blk/" + M["data"]["idd"])
                dicti = json.load(open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"]+".json", "r"))
                bls = int(dicti.get("bl", "0")) - 1
                dicti["bl"] = bls
                json.dump(dicti, open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"]+".json", "w"))

            else:
                open("ACCOUNTS/" + M["data"]["idd"] + "/blk/" + M["data"]["idd"], "w").write(M["data"]["idd"])
                dicti = json.load(open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"]+".json", "r"))
                bls = int(dicti.get("bl", "0")) + 1
                dicti["bl"] = bls
                json.dump(dicti, open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"]+".json", "w"))
            try:
                rson = json.load(open( "ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin", "").replace(".json", "") + ".json", "r"))
                blcs = int(rson.get("bl", "0")) + int(M["data"]["N"])
                rson["bl"] = str(blcs)
                json.dump(rson, open("ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/" + M["data"]["schm"].replace(".bin", "").replace(".json", "") + ".json","w"))
            except Exception as e :
                rson = json.load(open("ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/Activities/" + M["data"]["schm"].replace(".bin", "").replace( ".json", "") + ".json", "r"))
                blcs = int(rson.get("bl", "0")) + int(M["data"]["N"])
                rson["bl"] = str(blcs)
                json.dump(rson, open("ACCOUNTS_CHATS/" + M["data"]["zone"][0] + "/Activities/" + M["data"]["schm"].replace(".bin", "").replace( ".json", "") + ".json", "w"))

            rson = json.load(open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"][:8] + ".json", "r"))
            blcs = int(rson.get("bl", "0")) + int(M["data"]["N"])
            rson["bl"] = str(blcs)
            json.dump(rson, open("ACCOUNTS/" + M["data"]["idd"] + "/" + M["data"]["idd"][:8] + ".json", "w"))

            del dicti
            del bls
            del M
    except Exception as e :
        print(f"ER >>>> {e}",traceback.format_exc())

async def _files(dir,rev=True):
        FILES = [f.name for f in pathlib.Path(dir).iterdir()]
        FILES.sort(key=lambda x: os.stat(os.path.join(dir, x)).st_mtime, reverse=rev)
        return FILES

async def LK(M,writer):
    """Search In:
                organization message   Paid Adds message     zone       public talents   ACCOUNTS   PROFILE(BUSY).

    """

    IN=instancer
    ACC=await _files("TALENTS/"+M["data"]["ad"][0]+"/"+M["data"]["ad"][1])
    threading.Thread(target=IN,args=(M["data"]["kw"],ACC,M["data"]["ad"],M["recipients"]) ).start()

async def search_in_json(file_path, target_word):
    with open(file_path, 'r') as file:
        parser = ijson.parse(file)  # Incremental JSON parsing to save memory
        for prefix, event, value in parser:
            if isinstance(value, str) and target_word in value:
                pass

async def LOOKING_FOR(CM):
    OFFER_NEED = load_data("OFFER_NEED", {"LOOKING_FOR": {}, "OFFERING": {}})
    SENT=[]
    for jb in CM['data']["receiver"] :
        recipients= await _files("TALENTS/"+CM['data']["zone"][0]+"/"+ CM['data']["zone"][1]+"/"+jb)
        for rc in recipients :
            NCM=CM
            NCM["recipients"] =[rc]
            sidd=str(uuid.uuid4())[:8].replace("_", "").replace("-", "")  #  0784606767
            NCM["data"]["sidd"]=sidd
            NCM["deliver"] = sidd
            NCM["data"]["deliver"]=sidd
            # json.dump(CM, open("Temp_Emerg/" + sidd + ".json", "w"))
            if not rc in SENT:
                await Store(NCM)
                SENT.append(rc)

    jlist=CM["data"]["txt"].split()
    for jb in jlist:
        if OFFER_NEED["OFFERING"].get(jb.lower().strip() ,0):
            for rc in OFFER_NEED["OFFERING"][jb.lower().strip()]:
                NCM = CM
                NCM["recipients"] = [rc]
                sidd = str(uuid.uuid4())[:8].replace("_", "").replace("-", "")  # 0784606767
                NCM["data"]["sidd"] = sidd
                NCM["deliver"] = sidd
                NCM["data"]["deliver"] = sidd
                # json.dump(CM, open("Temp_Emerg/" + sidd + ".json", "w"))
                if not rc in SENT:
                    await Store(NCM)
                    SENT.append(rc)

            OFFER_NEED["OFFERING"][jb.lower().strip()].append(CM["data"]["idd"])
        else:
            OFFER_NEED["OFFERING"][jb.lower().strip()]=[]
            OFFER_NEED["OFFERING"][jb.lower().strip()].append(CM["data"]["idd"])
    pickle.dump(OFFER_NEED, open('OFFER_NEED', "wb"))
    del SENT

async def OFFERING(CM):
    OFFER_NEED = load_data("OFFER_NEED", {"LOOKING_FOR":{},"OFFERING":{}})
    SENT=[]
    for jb in CM['data']["receiver"] :
        recipients= await _files("TALENTS/"+CM['data']["zone"][0]+"/"+ CM['data']["zone"][1]+"/"+jb)
        for rc in recipients :
            NCM = CM
            NCM["recipients"] = [rc]
            sidd = str(uuid.uuid4())[:8].replace("_", "").replace("-", "")  # 0784606767
            NCM["data"]["sidd"] = sidd
            NCM["deliver"] = sidd
            if not rc in SENT:
                await Store(NCM)
                SENT.append(rc)

    jlist=CM["data"]["txt"].split()
    for jb in jlist:
        if OFFER_NEED["LOOKING_FOR"].get(jb.lower().strip() ,0):
            for rc in OFFER_NEED["LOOKING_FOR"][jb.lower().strip()]:
                NCM = CM
                NCM["recipients"] = [rc]
                sidd = str(uuid.uuid4())[:8].replace("_", "").replace("-", "")  # 0784606767
                NCM["data"]["sidd"] = sidd
                NCM["deliver"] = sidd
                if not rc in SENT:
                    await Store(NCM)
                    SENT.append(rc)
            OFFER_NEED["LOOKING_FOR"][jb.lower().strip()].append(CM["data"]["idd"])
        else:
            OFFER_NEED["LOOKING_FOR"][jb.lower().strip()] = []
            OFFER_NEED["LOOKING_FOR"][jb.lower().strip()].append(CM["data"]["idd"])
    pickle.dump(OFFER_NEED, open('OFFER_NEED', "wb"))
    del SENT
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

async def handle_client_connection(reader: StreamReader, writer: StreamWriter):
    global WRITER
    WRITER=writer
    try:
        data = await reader.read(1024)
        All = json.loads(data.decode())
    except json.JSONDecodeError as e:
        print("Error is : ",traceback.format_exc())
        writer.close()
        await writer.wait_closed()
        return

    if All.get("action", 0) == 'login':
        pass

    client_name = All["sender"]
    if not client_name in TOUS:
        TOUS.append(client_name)
    connected_clients[client_name] = writer

    print('WELCOME:   ',client_name)

    if client_name in offline_messages.keys():
        messages = offline_messages[client_name]
        for one in messages:
            if client_name in connected_clients:
                Nwriter=connected_clients[client_name]
                Nwriter.write(json.dumps({"sender": "server", "recipients": [client_name], "data": one}).encode("utf-8"))
                await Nwriter.drain()

    while True:
        try:
            data = await reader.read(6000)
            if data:
                try:
                    M = json.loads(data.decode())
                except:
                    M={}

                if M.get("action", 0) == "Received":
                    print("Received: ",M)
                    await Received2(M["deliver"])
                    # await received(M["deliver"])
                    M={}

                try:
                    s=M.get("sidd",None )
                    if s :
                        delivery={"_F_":s+".json"}
                        writer.write(json.dumps(delivery).encode("utf-8"))
                        await writer.drain()
                    else:
                        s = M.get("data", None)
                        if s:
                            delivery = {"_F_": M["data"].get("sidd", "")+".json"}
                            writer.write(json.dumps(delivery).encode("utf-8"))
                            print("delivery2: ", delivery)
                            await writer.drain()
                except Exception as e :
                    print("Delivery: ",e)



                if not M.get("deliver"):
                    if M.get("action") != "location" and len(M) != 0 :
                        if M.get("sidd",0):
                            M["deliver"]=M["sidd"]
                        else:
                            if M.get("data",0):
                                M["deliver"] = M["data"]["sidd"]
                            # else:
                            #     M["deliver"] = str(uuid.uuid4())[:12]

                if M.get("action", 0) == 'login':
                    if M["fun"] == "cred_name":
                        await cred_name(M["idd"], M["seg"], writer)
                    if M["fun"] == "cred_ok":
                        await cred_pwd(M, writer)
                #############################                 Emergency      ####################
                elif M.get("action",0) =="B_U" :                                               ##
                    # dic={"action":"ads","idd":M["data"]["idd"],"data":M["data"]}             ##
                    # await Store(dic)                                                         ##
                    await B_U(M)                                                               ##
                    M = {}                                                                     ##
                elif M.get("action",0) == "N_user" :                                           ##
                    await N_USER(M)                                                            ##
                    M = {}
                                                                                               ##
                elif M.get("action", 0) in ["inbx", "cht", "zone",'next',"next","contact","JB","lk","bl"] :
                    await ACTIVITY(M)                                                          ##
                                                                                               #
                    M={}

                elif M.get("action", 0) == "LK":
                    await LK(M, writer)

                elif M.get("action", 0) == "LOOKING_FOR":  #LOOKING_FOR    OFFERING
                    await LOOKING_FOR(M)
                elif M.get("action", 0) == "OFFERING":  #  "GVM"
                    await OFFERING(M)

                elif M.get("action", 0) == "GVM":  #  "GVM"
                    await Store(M)
                #################################################################################
                elif M.get("action", 0) == "New_client":
                    await NEW_CL(M)

                elif M.get("action", 0) == "trans":
                    await TRANSACTION(M)

                elif M.get("action", 0) == 'New_account':
                    await NEW_AC(M)

                elif M.get("action", 0) == 'UPDATES':
                    print("Updates")
                    await UPDATES(M)


                elif M.get("action", 0) == "New Alarm":
                    await NEW_ALR(M)
                    await keep(M)

                elif M.get("action", 0) == "token":
                    await TOKEN(M)

                elif M.get("action", 0) == "All_c":
                    await All_c(M, writer)

                elif M.get("action", 0) == "search":
                    await search(M, writer)

                elif M.get("action",0) == "one":
                    await ONE(M, writer)
                # else:
                    # print("M",M)
                    # if len(M) > 0 :
                    #     await keep(M)

                rec = M.get("recipients", [])
                for r in rec:
                    if r != M["sender"]:
                        if r in connected_clients.keys():
                            try:
                                connected_clients[r].write(data)
                                await connected_clients[r].drain()
                            except:
                                if not r in offline_messages.keys():
                                    offline_messages[r] = []
                                offline_messages[r].append(json.dumps(M))
                                del connected_clients[r]
                        else:
                            if not r in offline_messages.keys():
                                offline_messages[r] = []
                            offline_messages[r].append(json.dumps(M))

            else:
                if not await check_status(writer,client_name):
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except:
                        pass
                    break

        except Exception as e:
            print("ERROR: ",traceback.format_exc())
            # os.execl(sys.executable, sys.executable, *sys.argv)

            break
    try:
        writer.close()
        await writer.wait_closed()
    except:
        pass
    if client_name in connected_clients:
        del connected_clients[client_name]
    print(f"Client {client_name} disconnected")

async def send_chat_message(recipient: str, message: str):
    if recipient in connected_clients:
        writer = connected_clients[recipient]
        writer.write(json.dumps({'sender': 'Server', 'message': message}).encode())
        await writer.drain()
    else:
        if not recipient in offline_messages:
            offline_messages[recipient] = []
        offline_messages[recipient].append(message)

async def SENDER():
    sent=[]
    while True:
        try:
            files= await _files("Temp_Emerg/")
            for x in files:
                dct = json.load(open("Temp_Emerg/"+x, "r"))
                if not x in sent :
                    if dct["recipients"][0] in connected_clients:
                        writer=connected_clients[dct["recipients"][0]]
                        writer.write(json.dumps(dct).encode())
                        await writer.drain()
                        sent.append(x)
                        print("*** ",sent,"   x:  ",x)
                        del dct
                        del writer
                        x=None
                else:
                    os.remove("Temp_Emerg/"+x)
            files=[]
        except Exception as e:
            print("A MESSAGE WAS NOT SENT: ",e)
        sent=[]
        await asyncio.sleep(1)

async def forgoten():
    while True:
        try:
            for person in list(temporary.keys()):
                sms = temporary[person]
                for msg in sms:
                    writer = msg[0]
                    try:
                        writer.write(msg[1].encode("utf-8"))
                        await writer.drain()
                    except:
                        new_writer = connected_clients.get(person, None)
                        if new_writer:
                            try:
                                new_writer.write(msg[1].encode("utf-8"))
                                await new_writer.drain()
                            except:
                                pass
                        else:
                            if not offline_messages.get(person):
                                offline_messages[person] = []
                            offline_messages[person].append(json.dumps(msg[1]))
                del temporary[person]
        except:
            pass
        await asyncio.sleep(1)

async def Cleaner2():
    breath = '{"M":"online"}'
    try:
        while True:
            print("connected_clients", connected_clients)
            try:
                # Use a list to collect clients to delete to avoid modifying the dictionary while iterating
                to_delete = []
                for name, writer in connected_clients.items():
                    try:
                        writer.write(breath.encode("utf-8"))
                        await writer.drain()
                    except:
                        print(name, " deleted")
                        to_delete.append(name)
                        print("failed")

                # Remove disconnected clients after the iteration
                for name in to_delete:
                    del connected_clients[name]

            except Exception as e:
                print("Error in cleaner:", e)
            # time.sleep(3)
            # await asyncio.sleep(3)
    except:
        pass

async def cleaner():
    global  WRITER
    # breath = {"M":"online","recipients":TOUS}
    try:
        while True:
            if 'WRITER' in globals() and len(connected_clients)>0 :
                for cl in TOUS :
                    try:
                        breath = {"M": "ol", "tm":time.strftime("%d %B %Y %H:%M:%S"),"recipients": [cl]}
                        # WRITER.write(json.dumps(breath).encode())
                        # await WRITER.drain()
                    except Exception as e:
                        print("Error in cleaner:", e)
                        if cl in connected_clients:
                            try:
                                del connected_clients[cl]
                                print("DELETED: ",cl)
                            except Exception as e:
                                print("Failed to delete ",cl, "cause: ",e)

            await asyncio.sleep(3)
    except:
        pass

async def check_status(writer,client):
    try:
        writer.write(b'\n')
        await writer.drain()
        # print("The client is alive")
        return True
    except (ConnectionResetError, BrokenPipeError, asyncio.TimeoutError) as e :
        # print("The client is on broken pipe")
        return False

async def save():
    while True:     # TOUS
        pickle.dump(offline_messages, open('offline_messages', "wb"))
        pickle.dump(locations, open('locations', "wb"))
        pickle.dump(confirmed, open('confirmed', "wb"))
        pickle.dump(confirmed, open('save', "wb"))
        pickle.dump(TOUS, open('TOUS', "wb"))          #{"LOOKING_FOR":{},"OFFERING":{}}

        await asyncio.sleep(1)

async def main():
    server = await asyncio.start_server(handle_client_connection, HOST, PORT)
    print(f'Server running on http://{HOST}:{PORT}')
    threading.Thread(target=ftp).start()
    async with server:
        await asyncio.gather(server.serve_forever(),SENDER(), save(), forgoten(),cleaner() )             #  SENDER(),              #cleaner(),



if __name__ == '__main__':
    asyncio.run(main())
    unittest.main()


