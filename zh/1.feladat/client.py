import sys
import socket
import random
import struct
import time
import json


data = ""
with open('input.json') as json_file:
    data = json.load(json_file)

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect( (server_addr, server_port) )

packerClient = struct.Struct('c i')
packerServer1 = struct.Struct('2c i')
packerServer2 = struct.Struct('4c i')

print("Adja meg melyik függvényt szeretné használni: (f vagy g)")
f = input()
print("Adja meg a számot:")
x = input()
x = int(x)
msg = packerClient.pack(f.encode(), x)
sock.sendall(msg)
parsed_msg = ""
if x >= 0 and x <= 30:
    msg = sock.recv(packerServer1.size)
    parsed_msg = packerServer1.unpack( msg )
else:
    msg = sock.recv(packerServer2.size)
    parsed_msg = packerServer2.unpack( msg ) 
print(parsed_msg[2])
time.sleep(2)

# for nrnd in range(10):
# 	oper1 = random.randint(1,100)
# 	oper2 = random.randint(1,100)
# 	op = ops[nrnd % len(ops)]

# 	msg = packer.pack(oper1, oper2, op.encode())
# 	print( "Üzenet: %d %c %d" % (oper1, op, oper2) )	
# 	sock.sendall( msg )

# 	msg = sock.recv(packer.size)
# 	parsed_msg = packer.unpack( msg )
# 	print( "Kapott eredmény: %d" % parsed_msg[0])
# 	time.sleep(2)
sock.close()