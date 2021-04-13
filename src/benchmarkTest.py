# -*- coding: UTF-8 -*-
import sys
import time
import socket
from threading import Thread

HOST = "192.168.11.98"
PORT = int(sys.argv[1])
CONN = int(sys.argv[2])
MSGCUT = int(sys.argv[3])

threadQueue = []


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    count = 0
    for x in range(MSGCUT):
        # print(count)
        msg = bytes("this benchmark test #{}".format(count), 'utf-8')
        s.send(msg)
        count += 1
    # s.close()
    print("client close")


for x in range(CONN):
    threadQueue.append(Thread(target=client).start())
