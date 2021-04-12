# -*- coding: UTF-8 -*-
import sys
import socket
import time
from threading import Thread

HOST = 'localhost'
PORT = int(sys.argv[1])

queue = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
queue.append(s)
print("add client to queue")


def socketRecv():
    data = s.recv(1024).decode("utf-8")
    print(data)
    time.sleep(0.1)


def inputJob():
    data = input()
    s.send(bytes(data, "utf-8"))
    time.sleep(0.1)


while True:
    time.sleep(0.1)
    Thread(target=socketRecv).start()
    Thread(target=inputJob).start()


s.close()  # 關閉連線
