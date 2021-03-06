# -*- coding: UTF-8 -*-
import sys
import socket
import time
import threading
import select
import os

HOST = '192.168.11.98'
PORT = int(sys.argv[1])

queue = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
queue.append(s)
print("add client to queue")

sendMsgQueue = []


def inputJob():
    try:
        while True:
            data = input()
            sendMsgQueue.append(data)
    except EOFError:
        print("")


inputThread = threading.Thread(target=inputJob)
inputThread.start()

try:
    while True:
        readable, writable, _ = select.select([s], [], [], 0.00001)
        for sock in readable:
            data = sock.recv(1024)
            if data:
                data = data.decode("utf-8")
                print(data)
            else:
                # disconnect
                raise ConnectionAbortedError("disconnect")

        for msg in sendMsgQueue:
            s.send(bytes(msg, "utf-8"))
            sendMsgQueue.remove(msg)

except (KeyboardInterrupt):
    print("keyboardInterrupt")
    s.close()
except ConnectionAbortedError:
    print("disconnect")
finally:
    print("connect is close")
    os._exit(0)
