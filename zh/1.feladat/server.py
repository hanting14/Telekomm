import sys
import socket
import struct

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind( (server_addr, server_port) )

sock.listen(1)

packerClient = struct.Struct('c i')
packerServer1 = struct.Struct('2s i')
packerServer2 = struct.Struct('4s i')

conn, addr = sock.accept()
print("Valaki csatlakozott:", addr)
while True:
    msg = conn.recv(100)
    if not msg:
        print("A kliens lezárta a kapcsolatot")
        break
    parsed_msg = packerClient.unpack(msg)
    print((parsed_msg[0]).decode())
    print(parsed_msg[1])
    x = parsed_msg[1]
    if x >= 0 and x <= 30:
        if (parsed_msg[0]).decode() == 'f':
            x = 3*x + 4
        elif (parsed_msg[0]).decode() == 'g':
            x = pow(2, x) - 1
        text = "OK"
        msg = packerServer1.pack(text.encode(), x)
    else:
        text = "HIBA"
        msg = packerServer2.pack(text.encode(), 0)
    print(x)
    conn.sendall(msg)
    # print("Elküldött válasz: %d" % result)

conn.close()
sock.close()