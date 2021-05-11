import sys
import socket
import struct
import select
from random import randint

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind( (server_addr, server_port) )

sock.listen(10)

packer = struct.Struct('c i')

inputs = [ sock ]

gameEnd = False
randomNumber = randint(1,100)

try:
    while True:
        try:
            readables, _, _ = select.select( inputs, [], [] )
            print(randomNumber)
            for s in readables:
                if s is sock:
                    connection, client_info = sock.accept()
                    print("Csatlakozott valaki: %s:%d" % client_info )
                    inputs.append(connection)
                else:
                    data = s.recv(packer.size)
                    if not data:
                        s.close()
                        print("A kliens lezárta a kapcsolatot")
                        inputs.remove(s)
                        continue
                    msg = packer.unpack(data)
                    character = ""
                    if gameEnd:
                        character = "V"
                    elif msg[0].decode() == "=":
                        if msg[1] == randomNumber:
                            character = "Y"
                            gameEnd = True
                        else:
                            character = "K"
                    elif msg[0].decode() == "<":
                        if msg[1] > randomNumber:
                            character = "I"
                        else:
                            character = "N"
                    elif msg[0].decode() == ">":
                        if msg[1] < randomNumber:
                            character = "I"
                        else:
                            character = "N"
                    backmsg = packer.pack(character.encode(), msg[1])
                    s.sendall(backmsg)
                    print(character, msg[1])
            if len(inputs) == 1 and gameEnd:
                randomNumber = randint(1,100)
                gameEnd = False
        except:
            for s in inputs:
                s.close()
            #print("Server closing")
            break
finally:
    sock.close()
