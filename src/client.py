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

sendMsgQueue = []


def inputJob():
    try:
        while True:
            data = input()
            sendMsgQueue.append(data)
    except EOFError:
        print("A")


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

        for msg in sendMsgQueue:
            s.send(bytes(msg, "utf-8"))
            sendMsgQueue.remove(msg)

except KeyboardInterrupt:
    print('in except')
    s.close()
    inputThread.join()
    print("close")
