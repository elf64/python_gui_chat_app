import socket
import time
import threading
import string
from select import select
import json
import sys

s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

GLOBAL_MESSAGE = ['']
host = '192.168.0.4'
port = 9999
s.bind((host, port))
s.listen(5)
print("Listening on {}".format(s.getsockname()))
socket_list = []
connected_list = []
name_list = []

def on_new_client(clientsocket, addr, x):
    socket_list.append(clientsocket)
    time.sleep(1)
    while 1:
        r, w, e, = select([clientsocket], [], [])
        try:
            if r:
                msg = clientsocket.recv(1024)
                msg_decoded = msg.decode("utf-8")
                msg_chat = msg_decoded.split(" ")
                if msg_decoded.startswith(">>>>>>"):
                    msg_decoded = msg_decoded.replace(">>>>>>", "")
                    msg_json = json.loads(msg_decoded)
                    connected_list.append(msg_json['name'])
                    print(msg_json['name'])
                    clientsocket.send("<<<<<<{}|Welcome!".format(connected_list).encode("utf-8"))
                    if len(socket_list) > 1:
                        for i in socket_list:
                            if i == clientsocket:
                                pass
                            else:
                                i.send(">>>>>>{}|{} HAS CONNECTED".format(connected_list, msg_json['name']).encode("utf-8"))
                elif msg_chat[1] == "/users":
                    print(msg.decode("utf-8"))
                    for i in socket_list:
                            i.send("Users Online: {}".format(','.join(connected_list)).encode("utf-8"))
                elif not msg:
                    quit(2)
                else:
                    print(msg.decode("utf-8"))
                    GLOBAL_MESSAGE.append(msg.decode("utf-8"))
                    for i in socket_list:
                        if i == clientsocket:
                            pass
                        else:
                            i.send(GLOBAL_MESSAGE[-1].encode("utf-8"))
                    del GLOBAL_MESSAGE[-1]
        except Exception as egg:
            socket_list.remove(clientsocket)
            connected_list.remove(msg_json['name'])
            for i in socket_list:
                i.send("<<<<<<{}|{} HAS BEEN DISCONNECTED".format(connected_list, msg_json['name']).encode("utf-8"))
            raise egg

while 1:
    clientsocket, addr = s.accept()
    t = threading.Thread(target=on_new_client, args=tuple((clientsocket, addr, 0)))
    t.start()
    print("Got connection from {}".format(str(addr)))
    time.sleep(0.01)
s.close()
