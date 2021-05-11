import sys
import json


with open(sys.argv[1], "r") as read_file:
    data = json.load(read_file)
    maxtime = data["simulation"]["duration"]
    reserved_switches = []
    reserved_route = {}
    operations = 1
    for i in range(1, maxtime+1):
        for j in range(len(data["simulation"]["demands"])):
            if data["simulation"]["demands"][j]["start-time"] == i:
                reserved = "sikertelen"
                for k in range(len(data["possible-circuits"])):
                    if data["possible-circuits"][k][0] == data["simulation"]["demands"][j]["end-points"][0] and data["possible-circuits"][k][-1] == data["simulation"]["demands"][j]["end-points"][1]:
                        #print(data["possible-circuits"][k])
                        index = 1
                        while index < len(data["possible-circuits"][k])-1 and data["possible-circuits"][k][index] not in reserved_switches:
                            index += 1
                        if index == len(data["possible-circuits"][k])-1:
                            reserved_switches += data["possible-circuits"][k][1:len(data["possible-circuits"][k])-1]
                            reserved_route[j] = data["possible-circuits"][k]
                            reserved = "sikeres"
                            #print(reserved_route)
                            break
                print(str(operations) + ".igény foglalás: " + data["simulation"]["demands"][j]["end-points"][0] + "<->" + data["simulation"]["demands"][j]["end-points"][1] + " st:" + str(i) + "-" + reserved) 
                operations += 1
            elif data["simulation"]["demands"][j]["end-time"] == i: 
                #print(reserved_route)
                if j in reserved_route:
                    for k in range(1, len(reserved_route[j])-1):
                        reserved_switches.remove(reserved_route[j][k])
                    del reserved_route[j]
                    print(str(operations) + ".igény felszabadítás: " + data["simulation"]["demands"][j]["end-points"][0] + "<->" + data["simulation"]["demands"][j]["end-points"][1] + " st:" + str(i))
                    operations += 1