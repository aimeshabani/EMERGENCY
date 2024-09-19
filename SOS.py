import threading
# from SERVICE import start
# th=threading.Thread(target=start,args=(1,) )
# th.start()
# th.join()
while True:
    try:
        from SERVICE import start
        start(1)
    except Exception as e :
        print("CLOSING: ",e)


