




import sys
import time
import os
import unittest
import asyncio
import json
from plyer import notification
from plyer import audio
import ftplib
import pickle
import threading
from kivy.utils import platform
from datetime import datetime,timedelta
from kivy.logger import Logger           ##  Logger.info("GalleryApp: Opening gallery.")
from kivy.config import Config
import traceback
import uuid



def dr():
    try:
        from jnius import autoclass
        Env = autoclass('android.os.Environment')
        sd0 = Env.getExternalStorageDirectory().getAbsolutePath()
        directory = "Documents/org/SOS/"
        sd = os.path.join(sd0, directory)
        if not os.path.exists(sd):
            os.makedirs(sd)
        if not os.path.isdir(sd + "conf/"):
            os.mkdir(sd + "conf/")
        if not os.path.isdir(sd + "contacts/"):
            os.mkdir(sd + "contacts/")
        if not os.path.isdir(sd + "Items/"): #"Activities/"
            os.mkdir(sd + "Items/")
        if not os.path.isdir(sd + "Activities/"): #dr()+"Temp/"
            os.mkdir(sd + "Activities/")
        if not os.path.isdir(sd + "Temp/"):
            os.mkdir(sd +"Temp/")
        return sd
    except:
        sd="SD/"
        if not os.path.isdir(sd + "conf/"):
            os.mkdir(sd + "conf/")
        if not os.path.isdir(sd + "contacts/"):
            os.mkdir(sd + "contacts/")
        if not os.path.isdir(sd + "Items/"):
            os.mkdir(sd + "Items/")
        if not os.path.isdir(sd + "Activities/"): #
            os.mkdir(sd + "Activities/")
        if not os.path.isdir(sd + "Temp/"):
            os.mkdir(sd +"Temp/")
        return sd

try:
    HOST = json.load(open("SD/conf/server.json", "r"))
    HOST = HOST["ch_url"]
    PORT = json.load(open("SD/conf/server.json", "r"))
    PORT = PORT["port"]
except:
    HOST = "0.0.0.0"
    PORT = 8080
print("HOST: ", HOST, " PORT: ", PORT)




if platform == 'android':

    from jnius import autoclass
    import time
    import wave
    import threading
    import os
    import pickle

    AudioRecord = autoclass('android.media.AudioRecord')
    AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
    AudioFormat = autoclass('android.media.AudioFormat')
    ByteBuffer = autoclass('java.nio.ByteBuffer')


    class AudioRecorderService:
        def __init__(self):
            print("__init__")
            Environment = autoclass('android.os.Environment')
            File = autoclass('java.io.File')
            storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
            self.file_path = os.path.join(storage_path, "data/test")  # Adjust the path as needed

            self.sample_rate = 44100
            self.channel_config = AudioFormat.CHANNEL_IN_MONO
            self.audio_format = AudioFormat.ENCODING_PCM_16BIT
            self.buffer_size = AudioRecord.getMinBufferSize(self.sample_rate, self.channel_config, self.audio_format)
            self.audio_record = AudioRecord(
                AudioSource.MIC,
                self.sample_rate,
                self.channel_config,
                self.audio_format,
                self.buffer_size
            )
            self.frames = []

        def mic_callback(self, audio_data):
            print("mic_callback")
            self.frames.append(audio_data)
            print("self.frames ", self.frames)

        def record_audio(self):
            print("record_audio")

            self.frames = []
            self.audio_record.startRecording()

            for _ in range(0, int(self.sample_rate / self.buffer_size * 5)):
                audio_data = ByteBuffer.allocateDirect(self.buffer_size)
                self.audio_record.read(audio_data, self.buffer_size)
                self.mic_callback(audio_data.array())

            self.audio_record.stop()
            self.audio_record.release()

            print("Save the recorded frames to a .wav file")
            asyncio.run(BYTES(self.frames))


    from plyer import gps
    from jnius import autoclass
    from oscpy.server import OSCThreadServer
    from oscpy.client import OSCClient
    from plyer import vibrator as vib
    from plyer import notification
    import uuid


    def To_server(data):
        print("DATA: ",data)
        try:
            data=json.loads(data.decode('utf-8'))
            r=data.get("recipients",[me] )
            action=data.get("action",0)
            idd=data.get("idd","0788835687")
            data2={"action":action,"recipients": r,"data":data,"idd":idd,"sender":data.get("sender","")}

            if not os.path.isdir("offline2/"):
                os.mkdir("offline2")

            if data.get("action",0)=="token" :
                asyncio.run(send_chat_message(data2))
            if data.get("domain",0):
                asyncio.run(send_chat_message(data2,path="offline2/"+data["idd"]+"@"+data["domain"]+".json"))
            else:
                asyncio.run(send_chat_message(data))
        except Exception as e:
            print("FALLURE IN To_server: ", e)

    def from_main(r):
        try:
            import pickle
            # x=pickle.load(open("pickled", "rb"))
            #
            # print("rrrrrrrrrr",x)

            vib.vibrate(1/100)
            data = json.loads(r.decode())
            if not os.path.isfile(dr() + data["path"]):
                json.dump(data["data"], open(dr() + data["path"], "w"))
            else:
                msg='{"tt":"Warning","msg":"the file exist"}'
                # CLIENT.send_message( b'/message',[msg.encode('utf8'),],)
            print("okay")
        except Exception as e:
            print("FALLURE IN To_server: ", e)

    def call_main(x):
        vib.vibrate(1 / 60)
        X = json.dumps(x)
        CLIENT.send_message(b'/RECEIVER', [X.encode('utf8'), ], )

    try:
        CLIENT = OSCClient('localhost', 3002)

        # vib.vibrate(1/40)
        Env = autoclass('android.os.Environment')
        sd0= Env.getExternalStorageDirectory().getAbsolutePath()
        directory="Documents/org/SOS/"
        sd = os.path.join(sd0, directory)
        # if not os.path.exists(sd):
        #     os.makedirs(sd)
        # if not os.path.isdir(sd+"conf/"):
        #     os.mkdir(sd+"conf/")
        # if not os.path.isdir(sd+"contacts/"):
        #     os.mkdir(sd+"contacts/")
        # if not os.path.isdir(sd + "ready/"):
        #     os.mkdir(sd + "ready/")
        # # open(sd + "sd.txt", 'w').write(sd)


        # Env=autoclass('android.os.Environment')
        SERVER = OSCThreadServer()
        SERVER.listen('localhost', port=3000, default=True)
        SERVER.bind(b'/from_main', from_main)
        SERVER.bind(b'/To_server', To_server)
    except Exception as e:
        print("FALLURE IN root if platform == android: ", e)
    ME = json.load(open("SD/conf/me.json", "r"))


else:
    sd= "./SD/"
    # HOST = "0.0.0.0"
    # PORT = 8080
    ME = json.load(open("SD/conf/me.json", "r"))



me = ME["idd"]
pseudo = ME["pseudo"]

# me = json.load(open(dr()+"conf/me.json", "r"))["idd"]
# pseudo = json.load(open(dr()+"conf/me.json", "r"))["pseudo"]


RRR = []
TTT = 0
ALL = {}
All_c = None
DATAS = {}
alias=None
one=None
ERRORS=[]


def Vibrator(dc,t=1/40,r=6,sl=10):

    try:
        for x in range(r):
            for i in range(r):
                if platform == 'android':
                    vib.vibrate(time=t)
                time.sleep(t)
            time.sleep(sl)
            print("SET A RING")
            if not os.path.isfile(sd + "ready/"+dc["idd"]+".json"):
                break
    except Exception as e :
        print("CAUSE: ",e)

if not os.path.isdir("History"):
    os.mkdir("History")
res = {"status":"happy","aime":"0"}

Config.set('kivy','log_dir',dr()+'kivy/')

def alarm(presq=False):
    while True :
        AL= os.listdir("REMINDERS")
        for x in AL :
            if x.endswith(".json"):
                try:
                    dct=json.load(open("REMINDERS/"+x,"r"))
                    if dct["reminder frequency"] == "once" :
                        now = datetime.now()
                        last5 = now - timedelta(minutes=5)
                        ago = last5.strftime("%M")

                        le=len(dct["time"])
                        ls=[]
                        for i in dct["time"] :
                            if time.strftime("%"+i) == dct["time"][i]:
                                ls.append(i)
                                le=le-1
                        if le ==0 :
                            Vibrator(dc=dct,r=8)
                            asyncio.run( sound(len=3))
                            asyncio.run( al_list5(dct,dl=x))

                    else:
                        now = datetime.now()
                        last5 = now - timedelta(minutes=5)
                        ago = last5.strftime("%M")
                        # bck = dct["time"]["dispo"]
                        # del dct["time"]["dispo"]
                        le = len(dct["time"])
                        ls = []
                        for i in dct["time"]:
                            if time.strftime("%" + i) == dct["time"][i]:
                                ls.append(i)
                                le = le - 1
                        if le == 0:
                            Vibrator(dc=dct, r=8)
                            asyncio.run(sound(len=3))
                            asyncio.run(al_list5(dct))

                except Exception as e :
                    print(f"condition failed : {e}")

async def al_list5(dc,dl=None,online=None):  #  REMEMBER ONLINE RAPPEL, ITS ONE TOO AND HAVE NO FILE, ONLY CALL VIB


        if os.path.isfile(sd + "ready/"+dc["idd"]+".json") and not online :
            return
        if online :
            try:
                json.dump(dc, open(sd + "ready/" + dc["idd"] + ".json", "w"))
                await Vibrator(dc=dc)
            except:
                json.dump(dc, open("REMINDERS/" + dc["idd"] + "@" + dc["data"]["domain"] + ".json", "w"))
            await _vibratores(r=8)
        else:
            try:
                if not os.path.isfile(sd + "ready/" + dc["idd"] + ".json"):
                    json.dump(dc, open(sd + "ready/" + dc["idd"] + ".json", "w"))
                    Vibrator(dc=dc, r=8)
            except:
                pass

        if dl :
            os.remove("REMINDERS/"+dl)

async def call_main(x):
    X=json.dumps(x)
    CLIENT.send_message(b'/RECEIVER', [X.encode('utf8'), ], )

async def vibrator(t):
    vib.vibrate(time=t)

async def _vibratores(t=1/40,r=4):
    ERRORS.append("In _vibratores")
    if platform == "android" :
        for i in range(r):
            vib.vibrate(time=t)
            time.sleep(t)
# async def Vibrator(dc,t=1/40,r=6,sl=10):
#     print("SET A RING")
#     # if platform == "android" :
#     for x in range(r):
#         for i in range(r):
#             vib.vibrate(time=t)
#             time.sleep(t)
#         time.sleep(sl)
#         if not os.path.isfile(sd + "ready/"+dc["idd"]+".json"):
#             break
async def ringtone(kind):
    audio.play(kind)  # "ring/bell.ogg"

async def store(data):
    global RRR
    RRR.append(data)  # Communicate with main without writing files in real-time
    print("len(RRR) : ", len(RRR), RRR)

async def store2(data):
    global RRR
    RRR = data
    print("len(RRR) : ", len(RRR), RRR)

async def check_network(writer):
    try:
        writer.write(b'\n')
        await writer.drain()
        return True
    except (ConnectionResetError, BrokenPipeError, asyncio.TimeoutError) as e :
        return False

async def sound(typ="rm.ogg",len=1):
    if platform=="android":
        for i in range(len):
            try:
                MediaPlayer = autoclass('android.media.MediaPlayer')
                AudioManager = autoclass('android.media.AudioManager')
                Environment = autoclass('android.os.Environment')
                File = autoclass('java.io.File')

                # Get the path to the external storage directory
                storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
                file_path = os.path.join(storage_path, "data/"+typ)  # Adjust the path as needed

                # Check if the file exists
                file = File(file_path)
                if not file.exists():
                    print(f"File not found: {file_path}")
                    return

                # Initialize MediaPlayer and set data source
                mPlayer = MediaPlayer()
                mPlayer.setDataSource(file_path)
                mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
                mPlayer.prepare()
                mPlayer.start()

                # Wait for the audio to finish playing
                while mPlayer.isPlaying():
                    time.sleep(1)

                mPlayer.release()
                print(f"Playing file: {file_path}")
            except Exception as e:
                print(f"Error occurred: {e}")
    else:
        pass
        # audio.play(typ)

async def record_voice(file_name="test_record.mp4", duration=5):
    recorder_service = AudioRecorderService()
    recording_thread = threading.Thread(target=recorder_service.record_audio)
    recording_thread.start()

async def Record_voice2(file_name="test_record.mp4", duration=5):
    try:
        MediaRecorder = autoclass('android.media.MediaRecorder')
        AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
        OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
        AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
        Environment = autoclass('android.os.Environment')

        # Get the path to the external storage directory
        storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
        file_path = os.path.join(storage_path, "data", file_name)  # Adjust the path as needed

        # Create directories if they don't exist
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        # Initialize MediaRecorder
        mRecorder = MediaRecorder()
        mRecorder.setAudioSource(AudioSource.MIC)
        mRecorder.setOutputFormat(OutputFormat.MPEG_4)
        mRecorder.setOutputFile(file_path)
        mRecorder.setAudioEncoder(AudioEncoder.AAC)

        # Prepare and start recording
        mRecorder.prepare()
        mRecorder.start()

        # Record for the specified duration
        time.sleep(duration)

        # Stop and release the recorder
        mRecorder.stop()
        mRecorder.release()

        print(f'Recording saved to {file_path}')
        return file_path
    except Exception as e:
        print(f'Error occurred while recording: {e}')
        return None

async def SOUND(typ=None):
    try:
        MediaRecorder = autoclass('android.media.MediaRecorder')
        AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
        OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
        AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
        Environment = autoclass('android.os.Environment')

        # Get the path to the external storage directory
        storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
        output_file = f'{storage_path}/tst.mp3'

        # Create MediaRecorder instance
        mRecorder = MediaRecorder()
        mRecorder.setAudioSource(AudioSource.MIC)
        mRecorder.setOutputFormat(OutputFormat.MPEG_4)
        mRecorder.setOutputFile(output_file)
        mRecorder.setAudioEncoder(AudioEncoder.AMR_NB)

        # Prepare and start recording
        mRecorder.prepare()
        mRecorder.start()

        # Record for 5 seconds
        time.sleep(5)

        # Stop and release the recorder
        mRecorder.stop()
        mRecorder.release()

        print(f'Recording saved to {output_file}')
    except Exception as e:
        print(f'Error occurred: {e}')
    # from RECORD_AUDIO import start
    # start()


def his(data):
    if not data.get("st",0):
        return

    # "path":[time.strftime("%Y"),time.strftime("%B"),time.strftime("%d"),time.strftime("%H:%M:%S")]
    try:
        Y = json.load(open("History/"+data["st"], "r"))
        if not Y.get(data["path"][0],0):
            Y[data["path"][0]]={"TOTAL":"0"}
        if not Y[data["path"][0]].get(data["path"][1],0):
            Y[data["path"][0]][data["path"][1]]={"TOTAL":"0"}
        if not Y[data["path"][0]] [data["path"][1]].get(data["path"][2],0):
            Y[data["path"][0]][data["path"][1]] [data["path"][2]] ={"TOTAL":"0"}
        # if not Y[data["path"][0]][data["path"][1]][data["path"][3]].get(data["path"][3], 0):
        #     Y[data["path"][0]][data["path"][1]][data["path"][2]][data["path"][3]] = {"TOTAL":"0"}


        TD=float(Y[data["path"][0]][data["path"][1]][data["path"][2]]["TOTAL"])+ float(data["sum"])
        TM = float(Y[data["path"][0]][data["path"][1]]["TOTAL"]) + float(data["sum"])
        TY= float(Y[data["path"][0]]["TOTAL"]) + float(data["sum"])

        Y[data["path"][0]][data["path"][1]][data["path"][2]][data["path"][3]]=float(data["sum"])
        Y[data["path"][0]][data["path"][1]][data["path"][2]]["TOTAL"]=TD
        Y[data["path"][0]][data["path"][1]]["TOTAL"] = TM
        Y[data["path"][0]]["TOTAL"] = TY

        json.dump(Y,open("History/"+data["st"], "w"))
    except Exception as e :
        print("RESON TO FAIL: ",e)

async def Job(data):
    """d = {"schm": "ab", "action": OF_ND.replace(" ", "_"), "receiver": self.ME["jb"],
                     "zone": self.ME["adress"], 'sidd': sidd, 'idd': self.ME["idd"],"delete":DEL.ids["sidd"]}"""
    try:
        if data["data"].get("delete",0):
            if os.path.isfile(data["data"]["zone"][1] + "/" + data["action"].replace("_", " ") + "/jobs/" + data["data"]["delete"]):
                os.remove(data["data"]["zone"][1] + "/" + data["action"].replace("_", " ") + "/jobs/" + data["data"]["delete"])
                if platform == "android":
                    await call_main(data)
                else:
                    json.dump(data, open(dr() + "New_temp/" + data["data"]["sidd"] + ".json", "w"))
                print(data["data"]["delete"] , " deleted")
            return
    except Exception as e :
        print(f"PROBLEM WHEN DELETING: {e}", traceback.format_exc())
    try:
        if not os.path.exists(data["data"]["zone"][1] + "/" + data["action"].replace("_", " ")+"/jobs/"):
            os.makedirs(data["data"]["zone"][1]+ "/" + data["action"].replace("_", " ")+"/jobs/")
        if platform == "android":
            open(data["data"]["zone"][1] + "/" + data["action"].replace("_", " ") + "/jobs/" + data["data"]["sidd"], "w").write(str(data["data"]))
            await call_main(data)
        else:
            open(data["data"]["zone"][1] + "/" +data["action"].replace("_", " ") + "/jobs/" + data["data"]["sidd"], "w").write(str(data["data"]))
            json.dump(data, open(dr() + "New_temp/" + data["data"]["sidd"] + ".json", "w"))
    except Exception as e :
        print(f"PROBLEM {e}",traceback.format_exc())

async def GVM(data):
    try:
        if not os.path.exists(ME["adress"][1] + "/" + data["data"]["a2"]+"/bagainers/"+data["data"]["jb"]+"/"):
            os.makedirs(ME["adress"][1] + "/" + data["data"]["a2"]+"/bagainers/"+data["data"]["jb"]+"/")
        if platform == "android":
            open(ME["adress"][1] + "/" + data["data"]["a2"]+"/bagainers/"+data["data"]["jb"]+"/"+data["data"]["idd"], "w").write(str(data["data"]))
            await call_main(data)
        else:
            open(ME["adress"][1] + "/" + data["data"]["a2"]+"/bagainers/"+data["data"]["jb"]+"/"+data["data"]["idd"], "w").write(str(data["data"]))
            json.dump(data, open(dr() + "New_temp/" + data["data"]["sidd"] + ".json", "w"))
    except Exception as e :
        print(f"PROBLEM {e}",traceback.format_exc())

async def Emergency(data):

    if data.get("action",0)== "blc":
        acc=json.load(open("SD/conf/me.json","r"))
        blcs=int(acc.get("bl","0"))+int(data["data"]["bl"])
        acc["bl"]=str(blcs)
        json.dump(acc,open("SD/conf/me.json","w"))
        open(".bl/" + data["data"]["idd"], "w").write(data["data"]["schm"])

        if "contacts/" in data["data"]["schm"]:
            rson = pickle.load(open(dr()+data["data"]["schm"].replace(".bin", "").replace(".json", "")+".bin", "rb"))
            blcs = int(rson.get("bl", "0")) + int(data["data"]["bl"])
            rson["bl"] = str(blcs)
            pickle.dump(rson, open(dr()+data["data"]["schm"].replace(".bin", "").replace(".json", "")+".bin", "wb"))
        else:
            rson = pickle.load(open(dr() + "Activities/"+data["data"]["schm"], "rb"))
            blcs = int(rson.get("bl", "0")) + int(data["data"]["bl"])
            rson["bl"] = str(blcs)
            pickle.dump(rson, open(dr()+data["data"]["schm"].replace(".bin", "").replace(".json", "") + ".bin", "wb"))

    if data.get("action", 0) == "lk":
        acc = json.load(open("SD/conf/me.json", "r"))
        lks = int(acc.get("lk", "0")) + int(data["data"]["lk"])
        acc["lk"] = str(lks)
        json.dump(acc, open("SD/conf/me.json", "w"))
        open(".lk/" + data["data"]["idd"], "w").write(data["data"]["schm"])

        if "contacts/" in data["data"]["schm"]:
            rson = pickle.load(open(dr()+data["data"]["schm"].replace(".bin", "").replace(".json", "")+".bin", "rb"))
            lks = int(rson.get("lk", "0")) + int(data["data"]["lk"])
            rson["lk"] = str(lks)
            pickle.dump(rson, open(dr()+data["data"]["schm"].replace(".bin", "").replace(".json", "") + ".bin", "wb"))
        else:
            rson = pickle.load(open(dr() + "Activities/"+data["data"]["schm"], "rb"))
            lks = int(rson.get("lk", "0")) + int(data["data"]["lk"])
            rson["lk"] = str(lks)
            pickle.dump(rson, open(dr() + data["data"]["schm"].replace(".bin", "").replace(".json", "") + ".bin", "wb"))

    if data.get("action",0) == "src" :

        if platform == "android":
            await call_main(data)
        else:
            json.dump(data, open(dr() + "New_temp/" + data["data"]["sidd"] + ".json", "w"))
        return

    if "Activities" in data["data"]["schm"]:
        if not os.path.exists(dr() + data["data"]["schm"].replace(".bin", "").replace(".json", "")):
            os.makedirs(dr() +  data["data"]["schm"].replace(".bin", "").replace(".json", ""))

        pickle.dump(data["data"],open(dr() +  data["data"]["schm"] + ".bin", "wb"))  # replace with pyzip

        if platform == "android":
            await call_main(data["data"])
        else:
            json.dump(data["data"], open(dr() + "New_temp/" + data["data"]["sidd"] + ".json", "w"))  # json
        return

    if not os.path.exists(dr()+"Activities/"+data["data"]["schm"].replace(".bin", "").replace(".json", "")):
        os.makedirs(dr()+"Activities/"+data["data"]["schm"].replace(".bin", "").replace(".json", ""))
    pickle.dump(data["data"],open(dr()+"Activities/"+data["data"]["schm"].replace(".bin", "").replace(".json", "")+".bin","wb"))        #     replace with pyzip

    if platform == "android" :
        await call_main(data["data"])
    else:
        json.dump(data["data"], open(dr() + "New_temp/" + data["data"]["sidd"] + ".json", "w"))  # json

async def receive_messages(reader, writer):                  #  KEEP DELETING VARIABLE FOR FAST MEMORY
    print("connected to host and port")
    global TTT, All_c, RRR, cnt, data, res,one
    counter=0
    ERRORS.append("In receive messages")
    while True:
        try:
            message = await reader.read(3000000000)
            if message:
                # print(message)
                SMS = message.decode("utf-8")
                if isinstance(SMS, str):
                    if "}{" in SMS:
                        SMS = SMS.replace("}{", "}##{").split("##")
                        for i in SMS:
                            dic = json.loads(i)
                            try:
                                DATAS[dic["data"].get("sidd",str(uuid.uuid4())[:8].replace("_", "").replace("-", ""))]=dic
                            except Exception as e :
                                DATAS[dic.get("sidd", str(uuid.uuid4())[:8].replace("_", "").replace("-", ""))] = dic
                    else:
                        dic = json.loads(SMS)
                        try:
                            DATAS[dic["data"].get("sidd", str(uuid.uuid4())[:8].replace("_", "").replace("-", ""))] = dic
                        except Exception as e:
                            DATAS[dic.get("sidd", str(uuid.uuid4())[:8].replace("_", "").replace("-", ""))] = dic
                else:
                    if isinstance(SMS, dict):
                        try:
                            DATAS[SMS["data"].get("sidd", str(uuid.uuid4())[:8].replace("_", "").replace("-", ""))] = SMS
                        except Exception as e:
                            DATAS[SMS.get("sidd", str(uuid.uuid4())[:8].replace("_", "").replace("-", ""))] = SMS

                for DC in DATAS.keys():
                    data=DATAS[DC]
                    # print("DATAS: ",DATAS)
                    if data.get("_F_",0):# from server/ delete local
                        if data["_F_"] == "" :
                            os.remove(i for i in dr() + "Temp/" )
                            print('data["_F_"]',data["_F_"])
                        else:
                            print('data["_F_"]', data["_F_"])
                            try:
                                if os.path.isfile(dr() + "Temp/" + data["_F_"]) :
                                    os.remove(dr() + "Temp/" + data["_F_"])
                                    print("File ",data["_F_"]," deleted")
                                    ERRORS.pop(-1) if len(ERRORS) > 0 else print()
                            except Exception as e :
                                print("Was there a file ? ....: ",e)
                                ERRORS.append("Was there a file ? ....: "+str(e))

                    if data.get("deliver",0):   #   to server/ delete from host
                        writer.write(json.dumps({"sender": me, "deliver": data["deliver"], "action": "Received"}).encode())
                        await writer.drain()
                        print('deliver:',data["deliver"],"data: ",data)
                        # data={}
                    # if not data.get("deliver"):
                    #     if len(data)== 0:
                    #         return
                    #     print("HERE ??")
                    #     if data.get("data"):
                    #         if isinstance(data["data"], str):
                    #             data3 = json.loads(data["data"])
                    #             if data3.get("deliver"):      #     offer_need has no deliver in data, then here it resends to server as message containing M["data"]
                    #                 writer.write(json.dumps({"sender": me, "deliver": data3["deliver"], "action": "Received"}))
                    #         if isinstance(data["data"], dict):
                    #             writer.write(json.dumps({"sender": me, "deliver": data["data"]["deliver"], "action": "Received"}))

                    if data.get("action") in ["inbx", "cht", "zone","next","B_U","blc","lk"]:
                        # Logger.info('["inbx", "cht", "zone"] ', data)
                        await Emergency(data)
                        await sound()

                    if data.get("action") in ["OFFERING" , "LOOKING_FOR"]:
                        await Job(data)

                    if data.get("action", 0) == "GVM":
                        await GVM(data)

                    if data.get("action") == "src":
                        # Logger.info('["inbx", "cht", "zone"] ', data)
                        await Emergency(data)

                    if data.get("action",0) == "contact" :
                        try:
                            print(dr()+"contacts/"+ data["contact"]["idd"] + ".json")

                            if not os.path.exists(dr()+"contacts/"+ data["contact"]["idd"]):
                                os.makedirs(dr()+"contacts/"+ data["contact"]["idd"])
                            json.dump(data["contact"],open( dr()+"contacts/"+ data["contact"]["idd"]+"/"+data["contact"]["idd"] + ".json", "w"))
                        except Exception as e:
                            print("Execption: ",e)

                    if data.get("action",0)!= "UPDATES2" :
                        # print("data: ",data)
                        pass

                    if data.get('action') != 'location':
                        pass

                    if data.get("action", 0) == "New Alarm" :
                        json.dump(data["data"], open("REMINDERS/" + data["idd"] + "@" + data["data"]["domain"] + ".json", "w"))
                        await sound()
                        await _vibratores()
                        # await call_main('{"mess":"home"}')

                    if data.get("action", 0) == "trigger" :  #"stop_auto_scroll"
                        await al_list5(data["data"],dl=1)
                        print()

                    if data.get("action2", 0) == "token" :  #
                        await sound()
                        json.dump(data["data"], open("tokens/" + data["idd"] + "@" + data["data"]["domain"] + ".json", "w"))
                        # open("stop_auto_scroll").write("ok")

                    if data.get("M", 0) == "ol":
                        # print("online: ",data["tm"]) #                   PUT SOUND HERE , AND REGESTER LAST ONLINE
                        pass

                    if data.get("message") == "Received":
                        pass
                    if data.get("action") == "rsp_login":
                        print(data)
                        TTT = data

                    if data.get("action") == "one":
                        # print("one in BACK ",data)
                        one = data

                    if data.get("action") == "s_r":
                        RRR.append(data["data"])

                    if data.get("action") == "find":
                        DTA=json.dumps(data)
                        CLIENT.send_message(b'/SEARCH', [DTA.encode('utf8'), ], )

                    if data.get("action") == "UPDATES2":
                        await sound()
                        if not data.get("data1"):
                            if data.get("data"):
                                if isinstance(data["data"], str):
                                    data3 = json.loads(data["data"])
                                    if data3.get("data1"):
                                        json.dump(data["data1"], open("History/" + data["tp"] + ".json", "w"))
                        else:
                            json.dump(data["data1"], open("History/" + data["tp"] + ".json", "w"))

                    if data.get("action") == "55":
                        await sound()
                        th=threading.Thread(target=his,args=(data,))
                        th.start()

                    if data.get("action") == "s_r_e":
                        RRR.append("stop")
                        pickle.dump(RRR, open("RRR", "wb"))
                    if data.get("action") == "ALL":
                        ALL = data
                    if data.get("action") == "All_c":
                        All_c = data

                    try:
                        del DATAS[DC]
                    except:
                        pass
            else:
                if not await check_network(writer):
                    res["status"]="pain"
                    await connector()
                print("Connection Lost reconnecting...")

        except OSError as e:
            # if e.errno == 103 :
                # sys.exit("EXITING ...")

            print("restarting...",e)
            ERRORS.append("restarting..."+str(e))
            if "Connection reset by peer" in e :
                Error=Do_not_exist
                # os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            if "Connection reset by peer" in str(e):
                Error = Do_not_exist
            ERRORS.append(f"Error BACK Receiver: {e}")
            # res["status"] = "pain"
            # asyncio.create_task(connector())     # WHY TO CALL  connector()   WHICH MEANS TO RECONNECT FOR AN ERROR IN MESSAGE ?
            # break

async def newms():
    global alias
    while True:
        if alias:
            await send_chat_message(alias)
            alias=None
        await asyncio.sleep(3)

async def BYTES(data):
    global res, writer
    w=pickle.dumps({"action": "byt", 'recipients': [me], "idd": me, "sender": me,"data":data})
    writer.write(w)
    await writer.drain()
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

async def send_chat_message(message=None,wrt=None,path=None):
    global res,writer,alias, one
    try:
        if wrt:
            writer=wrt
        if message:
            print("message: ",message)
            if message.get("action",0) == "one":
                one=None
            message["sender"] = me
            if not message.get("recipients",0):
                message["recipients"] = [me]

            if message["action"] == "location":
                data = json.dumps(message)
                try:
                    writer.write(data.encode())
                    await writer.drain()
                except:
                    try:
                        del res["aime"]
                    except:
                        pass
                    res["status"] = "pain"
                    asyncio.create_task(connector())
                return

            if message.get("acc", 0):
                if message["acc"].get("photo", 0):
                    bin = open(message["acc"]["photo"], "rb")
                    port = 2121
                    IP = HOST
                    srv = "aime shabani"
                    pwd = "12435687"
                    FTP = "C_IMG/"

                    ftp = ftplib.FTP()
                    ftp.connect(IP, port)
                    ftp.login(srv, pwd)
                    ftp.cwd(FTP)
                    ftp.storbinary("STOR " + message["acc"]["idd"] + "_" + message["acc"]["Name"] + "@" + message["acc"]["Post_Name"] + ".png", bin)
                    message["acc"]["photo"] = message["acc"]["idd"] + "_" + message["acc"]["Name"] + "@" + message["acc"]["Post_Name"] + ".png"
                    new = json.dumps(message)
                    try:
                        writer.write(new.encode())
                        await writer.drain()
                    except:
                        try:
                            del res["aime"]
                        except:
                            pass
                        res["status"] = "pain"
                        json.dump(message, open("offline/" + message["acc"]["idd"] + "_" + message["acc"]["Name"] + "@" + message["acc"]["Post_Name"] + ".json", "w"))
                        asyncio.create_task(connector())
                else:
                    data = json.dumps(message)
                    try:
                        writer.write(data.encode())
                        await writer.drain()
                    except:
                        try:
                            del res["aime"]
                        except:
                            pass
                        res["status"] = "pain"

                        json.dump(message, open("offline/" + message["acc"]["idd"] + "_" + message["acc"]["Name"] + "@" + message["acc"]["Post_Name"] + ".json", "w"))
                        asyncio.create_task(connector())

            # if message.get("action",0) =="B_U" :
            #     #########################################################################################
            #
            #     dt = message.get("sidd", None)
            #     if dt:
            #         if not os.path.isfile(dr() + "Temp/" + dt + ".json"):
            #             json.dump(message, open(dr() + "Temp/" + dt + ".json", "w"))
            #     else:
            #         dt = message.get("data", None)
            #         if dt:
            #             if not os.path.isfile(dr() + "Temp/" + dt["sidd"] + ".json"):
            #                 json.dump(message, open(dr() + "Temp/" + dt + ".json", "w"))
            #     #######################################################################################
            #
            #     if not message.get("data",0) :
            #         r = message.get("recipients", [me])
            #         action = message.get("action", 0)
            #         idd = message.get("idd", "0788835687")
            #         message = {"action": action, "recipients": r, "data": message, "idd": idd, "sender": message.get("sender", "")}
            #
            #     port = 2121
            #     IP = HOST
            #     srv = "aime shabani"
            #     pwd = "12435687"
            #     FTP = "ACCOUNTS/"+message["idd"]+"/Items"    #************************* COME BACK HERE
            #
            #     ftp = ftplib.FTP()
            #     ftp.connect(IP, port)
            #     ftp.login(srv, pwd)
            #     ftp.cwd(FTP)
            #
            #     for pht in message["data"]["pht"]:
            #         if not "ACCOUNTS/" in pht :
            #             pass
            #         else:
            #             if os.path.isfile(pht):
            #                 bin = open(pht, "rb")
            #                 ftp.storbinary("STOR " + message["data"]["sidd"]+".png", bin)
            #                 del bin
            #                 message["data"]["pht"].remove(pht)
            #                 message["data"]["pht"].append("ACCOUNTS/" + message["data"]["idd"] + "/" + "Items" + "/" + message["data"]["sidd"] + ".png")
            #
            #     if message["data"].get("BUSY", 0):
            #         if len(message["data"].get("BUSY", [])) > 0:
            #
            #             port = 2121
            #             IP = HOST
            #             srv = "aime shabani"
            #             pwd = "12435687"
            #             FTP = "ACCOUNTS/" + message["idd"] + "/Items"  # ************************* COME BACK HERE
            #
            #             ftp = ftplib.FTP()
            #             ftp.connect(IP, port)
            #             ftp.login(srv, pwd)
            #             ftp.cwd(FTP)
            #
            #             for pht in message["data"]["BUSY"]:
            #                 print("pht1", pht)
            #                 if len(pht) > 1:
            #                     dir = pht[1]
            #                 else:
            #                     dir = ""
            #                 if os.path.isfile(dir):
            #                     try:
            #                         bin = open(dir, "rb")
            #                         ftp.storbinary("STOR " + os.path.basename(dir), bin)
            #                         del bin
            #                         nl=[pht[0]]
            #                         nl.append("ACCOUNTS/" + message["data"]["idd"] + "/" + "Items" + "/" + os.path.basename(dir) )
            #                         message["data"]["BUSY"].remove(pht)
            #                         message["data"]["BUSY"].append(nl)
            #                         # message["data"]["BUSY"][pht]
            #                     except Exception as e:
            #                         print("Exceptino: ",e)
            #
            #     data = json.dumps(message)
            #     try:
            #         writer.write(data.encode())
            #         await writer.drain()
            #     except:
            #         try:
            #             del res["aime"]
            #         except:
            #             pass
            #         res["status"] = "pain"
            #
            #         json.dump(message, open("offline/" + message["data"]["sidd"] +  ".json", "w"))
            #         asyncio.create_task(connector())
            #     return

            #
            if message.get("schm",0) or message.get("action",0) in ["B_U","next","zone","cht","inbx", "N_user","lk","bl" ,'LOOKING_FOR', "OFFERING"] :

                ###########################################################################

                dt = message.get("sidd", None)
                if dt:
                    if not os.path.isfile(dr() + "Temp/" + dt + ".json"):
                        json.dump(message, open(dr() + "Temp/" + dt + ".json", "w"))
                else:
                    dt = message.get("data", None)
                    if dt:
                        if not os.path.isfile(dr() + "Temp/" + dt["sidd"] + ".json"):
                            json.dump(message, open(dr() + "Temp/" + dt + ".json", "w"))
                ##################################################################################



                if not message.get("data",0) :
                    r = message.get("recipients", [me])
                    action = message.get("action", 0)
                    idd = message.get("idd", "0788835687")
                    message = {"action": action, "recipients": r, "data": message, "idd": idd, "sender": message.get("sender", "")}

                if message["data"].get("pht",0) :
                    port = 2121
                    IP = HOST
                    srv = "aime shabani"
                    pwd = "12435687"
                    FTP = "ACCOUNTS/"+message["idd"]+"/Items"    #************************* COME BACK HERE

                    ftp = ftplib.FTP()
                    ftp.connect(IP, port)
                    ftp.login(srv, pwd)
                    ftp.cwd(FTP)


                    for pht in message["data"]["pht"]:
                        if "ACCOUNTS/" in pht:
                            pass
                        else:
                            if os.path.isfile(pht):
                                sidd=str(uuid.uuid4())[:5].replace("-","").replace(" ","").replace("_","")
                                bin = open(pht, "rb")
                                ftp.storbinary("STOR " + sidd+".png", bin)
                                del bin
                                message["data"]["pht"].remove(pht)
                                message["data"]["pht"].append("ACCOUNTS/"+message["data"]["idd"]+"/"+"Items"+"/"+ sidd +".png")  #  WHAT ABOUT 2 PHOTOS ? WILL THEY HAVE THE SAME NAME SIDD ?

                if message.get("data", 0):
                    if message["data"].get("BUSY", 0):
                        if len(message["data"].get("BUSY", [])) > 0:

                            port = 2121
                            IP = HOST
                            srv = "aime shabani"
                            pwd = "12435687"
                            FTP = "ACCOUNTS/" + message["idd"] + "/Items"  # ************************* COME BACK HERE

                            ftp = ftplib.FTP()
                            ftp.connect(IP, port)
                            ftp.login(srv, pwd)
                            ftp.cwd(FTP)

                            for pht in message["data"]["BUSY"]:
                                print("pht1", pht)
                                if len(pht)>1 :
                                    dir = pht[1]
                                else:
                                    dir=""
                                if os.path.isfile(dir):
                                    try:
                                        bin = open(dir, "rb")
                                        ftp.storbinary("STOR " + os.path.basename(dir), bin)
                                        del bin
                                        nl = [pht[0]]
                                        nl.append("ACCOUNTS/" + message["data"]["idd"] + "/" + "Items" + "/" + os.path.basename(dir))
                                        message["data"]["BUSY"].remove(pht)
                                        message["data"]["BUSY"].append(nl)
                                        # message["data"]["BUSY"][pht]
                                    except Exception as e:
                                        print("Exceptino: ", e)


                data = json.dumps(message)
                try:
                    writer.write(data.encode())
                    await writer.drain()
                except:
                    # try:
                        # json.dump(message, open("offline/" + message["data"]["sidd"] + ".json", "w"))
                    asyncio.create_task(connector())
                    # except:
                        # json.dump(message, open("offline/" + message["sidd"] + ".json", "w"))
                        # asyncio.create_task(connector())
                    try:
                        del res["aime"]
                    except:
                        pass
                    res["status"] = "pain"

            else:
                print("else:",message)
                ########################################################################

                dt = message.get("sidd", None)
                if dt:
                    if not os.path.isfile(dr() + "Temp/" + dt + ".json"):
                        json.dump(message, open(dr() + "Temp/" + dt + ".json", "w"))
                else:
                    dt = message.get("data", None)
                    if dt:
                        if not os.path.isfile(dr() + "Temp/" + dt["sidd"] + ".json"):
                            json.dump(message, open(dr() + "Temp/" + dt + ".json", "w"))
                #######################################################################
                if not message.get("data", 0):
                    r = message.get("recipients", [me])
                    action = message.get("action", 0)
                    idd = message.get("idd", "0788835687")
                    message = {"action": action, "recipients": r, "data": message, "idd": idd,
                               "sender": message.get("sender", "")}

                data = json.dumps(message)
                try:
                    writer.write(data.encode())
                    await writer.drain()
                except:                       #    (ConnectionResetError, BrokenPipeError, asyncio.TimeoutError) as e
                    print("No connection")
                    try:
                        del res["aime"]
                    except:
                        pass
                    res["status"] = "pain"
                    # if path:
                    #     json.dump(message, open(path, "w"))
                    # else:
                    #     id = message.get("idd", message.get("sender"))
                    #     json.dump(message, open("offline/" + id + ".json", "w"))
                    asyncio.create_task(connector())
    except Exception as e:
        print("DELETE THIS MESSAGE FROM Temp/: ", traceback.format_exc())
        print("FALLURE IN send_chat_message: ",e)

async def offline(main=None):
    print("offline")
    try:
        # ERRORS.append("in offline function")
        global writer
        if main:
            await send_chat_message(main, writer)
            return

        for c in os.listdir("offline"):
            dct = json.load(open("offline/" + c, "r"))
            if res["status"] == "happy":
                os.remove("offline/" + c)
                await send_chat_message(dct, writer)
                print("Sent from offline")
    except Exception as e:
        print("FALLURE IN offline : ",e)

async def periodic_updates(writer) :     #   Not a LOOP   CALL IT FROM MAIN AND OSC
    global res

    while True:
        for c in os.listdir(dr()+"Temp/"):
            dct = json.load(open(dr()+"Temp/" + c, "r"))
            await send_chat_message(dct, writer)

        await asyncio.sleep(1)

async def main():
    global res
    th=threading.Thread(target=alarm)
    th.start()
    await connector()

async def connector():
    global res, reader, writer, ERRORS
    while True:
        try:
            reader, writer = await asyncio.open_connection(HOST, PORT)
            res["status"] = "happy"
            res["aime"]="0"
            client_name = json.dumps({"sender": me})
            writer.write(client_name.encode())
            await writer.drain()
            await asyncio.gather(receive_messages(reader, writer),periodic_updates(writer), _vibratores() )

            break
        except Exception as e:
            res["status"] = "pain"
            try:
                del res["aime"]
            except:
                pass

            import sys

            ERRORS.append(f"Error in connector: {e}")
            if len(ERRORS)>20:
                print("ERRORS: ",ERRORS)
                ERRORS=[]
                print(f"Error in connector: {e}")
                error=my_error  #sys.exit("Gone")
                # print("ERRORS",ERRORS)
                # try:
                #     import sys
                #     import subprocess
                #     python = sys.executable
                #     print("SUBPROCESS",python,":")
                #     # subprocess.call([python] + sys.argv)
                # except:
                #     import sys
                #     import os
                #     python = sys.executable
                #     print("OS.EXECL",python,":")
                #     os.execl(python, python, *sys.argv)
                # sys.exit("EXIT...")
        await asyncio.sleep(5)

async def order(data=None):
    global All_c, writer
    if data:
        data = json.dumps(data)
        try:
            writer.write(data.encode())
            await writer.drain()
        except:
            res["status"] = "pain"
        while True:
            if All_c:
                x = All_c
                All_c = None
                return x

async def one_cl(data=None):
    global All_c, writer
    if data:
        data = json.dumps(data)
        try:
            writer.write(data.encode())
            await writer.drain()
        except:
            res["status"] = "pain"
        while True:
            if All_c:
                x = All_c
                All_c = None
                return x

def start(x):
    if x:
        asyncio.run(main())
    else:
        Make()

if __name__ == '__main__':
    start(True)


