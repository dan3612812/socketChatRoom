# -*- coding: UTF-8 -*-
import socket
import select
import sys
import traceback

HOST = '192.168.11.98'
PORT = int(sys.argv[1])
connectionList = []  # 紀錄連線後的client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("create socket")

try:
    server.bind((HOST, PORT))
except:
    print("bind port error")
print("bind host and port")

server.listen(10000)
print("socket listening")

connectionList.append(server)


def getAllConnect():
    msg = ""
    for sock in connectionList:
        if not sock is server:
            sc = sock.getpeername()
            addr = "{}:{}".format(sc[0], sc[1])
            msg += addr+"\n"
    return msg


def broadcast(typeMsg: str, message: str):
    # 將訊息傳給所有人
    for socket in connectionList:
        if not socket is server:
            try:
                msg = "[{typeMsg}]:{message}".format(
                    typeMsg=typeMsg, message=message)

                socket.send(bytes(msg, 'utf-8'))
            except:
               # 關閉該連線 移除標記
                socket.close()
                connectionList.remove(socket)


while True:
    readable, _, _ = select.select(connectionList, [], [], 1)
    for sock in readable:
        if sock is server:
            # 有client handshake
            client, addr = sock.accept()
            connectionList.append(client)
            print("client connection :{}".format(addr))
            client.send(bytes("welcome to yuntech bagayaro", 'utf-8'))
            broadcast("system", "client :{} connection.".format(addr))

        else:
            # client send message to server Or client socket be trigger
            try:
                data = sock.recv(1024)
                if not data:
                    # disconnect
                    connectionList.remove(client)
                else:
                    data = data.decode("utf-8")
                    if(data == "#clientList"):
                        print("client:{} use command \"#clientList\"".format(
                            sock.getpeername()))
                        sock.send(bytes(getAllConnect(), 'utf-8'))
                    else:
                        # client socket be trigger Or get client message
                        clientAddr = client.getpeername()
                        print("clientAddr:{clientAddr} send:{msg}".format(
                            clientAddr=clientAddr, msg=data))
                        broadcast("client {}".format(clientAddr), data)
            except Exception as e:
                error_class = e.__class__.__name__  # 取得錯誤類型
                detail = e.args[0]  # 取得詳細內容
                cl, exc, tb = sys.exc_info()  # 取得Call Stack
                lastCallStack = traceback.extract_tb(
                    tb)[-1]  # 取得Call Stack的最後一筆資料
                fileName = lastCallStack[0]  # 取得發生的檔案名稱
                lineNum = lastCallStack[1]  # 取得發生的行號
                funcName = lastCallStack[2]  # 取得發生的函數名稱
                errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
                    fileName, lineNum, funcName, error_class, detail)
                print(errMsg)
