import sys
import socket
import struct
import select

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind( (server_addr, server_port) )

sock.listen(5)

packerClient = struct.Struct('c i')
packerServer1 = struct.Struct('2s i')
packerServer2 = struct.Struct('4s i')

inputs = [ sock ]

while True:
    try:
        readables, _, _ = select.select( inputs, [], [] )
        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print("Csatlakozott valaki: %s:%d" % client_info )
                inputs.append(connection)
            else:
                msg = s.recv(packerClient.size)
                if not msg:
                    s.close()
                    print("A kliens lezárta a kapcsolatot")
                    inputs.remove(s)
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
                s.sendall(msg)
    except:
        for s in inputs:
            s.close()
        print("Server closing")
        break
    # print("Elküldött válasz: %d" % result)
