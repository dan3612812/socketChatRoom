# -*- coding: UTF-8 -*-
import sys
import socket
import time
import threading
import select

HOST = '192.168.11.98'
PORT = int(sys.argv[1])

queue = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
queue.append(s)
print("add client to queue")



def socketRecv():
    while True:
        data = s.recv(1024).decode("utf-8")
        print(data)
        time.sleep(0.1)


def inputJob():
    while True:
        data = input()
        s.send(bytes(data, "utf-8"))
        time.sleep(0.1)


socketThread = threading.Thread(target=socketRecv)
socketThread.start()
# inputThread = Thread(target=inputJob)
# inputThread.start()
try:
    while True:
        data = input()
        s.send(bytes(data, "utf-8"))
        time.sleep(0.1)
except KeyboardInterrupt or EOFError:
    print("in except")
    # s.close()  # 關閉連線
    socketThread.do_run = False
    # socketThread.join()
    # inputThread.join()
    print("close thread")
    sys.exit(0)
