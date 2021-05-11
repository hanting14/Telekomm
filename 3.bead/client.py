import sys
import socket
import random
import struct
import time
import math
from random import randint
from time import sleep

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

packer = struct.Struct('c i')
left = 1
right = 100
lastSign = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect( (server_addr, server_port) )   
    while True:
        m = math.floor((left+right) / 2)
        sign = ""
        if lastSign == 1:
            sign = ">"
            lastSign = 0
        elif lastSign == 0: 
            sign = "<"
            lastSign = 1
        if m == left and m == right:
            sign = "="
        msg = packer.pack(sign.encode(), m)
        print(sign, m, left, right)

        sleep(randint(1, 5))

        client.sendall(msg)

        try:
            data = client.recv(packer.size)
            if not data:
                print("Server down")
            else:
                backmsg = packer.unpack(data)
                if backmsg[0].decode() == "Y" or backmsg[0].decode() == "K" or backmsg[0].decode() == "V":
                    break
                if backmsg[0].decode() == "I":
                    if sign == "<":
                        right = m-1
                    elif sign == ">":
                        left = m+1
                elif backmsg[0].decode() == "N":
                    if sign == "<":
                        left = m
                    elif sign == ">":
                        right = m
        except:
            #print("A szerver lezárta a kapcsolatot")
            break