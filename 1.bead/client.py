import sys
from subprocess import PIPE, Popen
import json
from datetime import date

infile = open(sys.argv[1], "r")
input_data = []
lines = infile.readlines()
first_lines = lines[:10]
last_lines = lines[-10:]
lines = first_lines + last_lines
for i in range(0, 20):
    x = lines[i].split(",")
    input_data.append(x[1].rstrip())
    #print(input_data[i])
infile.close()
output_ping = {"date" : date.today().strftime("%Y%m%d"), "system" : sys.platform, "pings" : []}
output_trace = {"date" : date.today().strftime("%Y%m%d"), "system" : sys.platform, "traces" : []}
process = []
for i in range(20): #max active process
    p = Popen(["ping", '-n', '10', input_data[i]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    process.append(p)
    ures = False
while (not ures):
    fut = 0
    k = 0
    while(k < len(process)):
        if not process[k] is None:
            if process[k].poll() == None:
                fut += 1
            else:
                out, err = process[k].communicate()
                ping_data = {"target" : input_data[k] , "output" : out.replace("\n", " ").strip()}
                output_ping["pings"].append(ping_data)
                #print(str(process[k].communicate()).split(' ')[1])
                process[k] = None
        k += 1
    if (fut <= 0):
        ures = True

with open("ping.json", "w") as outfile:  
    json.dump(output_ping, outfile, indent = 1)

process = [] 
for i in range(20): #max active process
    q = Popen(["tracert", '/h', '30', input_data[i]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    process.append(q)
    ures = False
while (not ures):
    fut = 0
    k = 0
    while(k < len(process)):
        if not process[k] is None:
            if process[k].poll() == None:
                fut += 1
            else:
                out, err = process[k].communicate()
                trace_data = {"target" : input_data[k], "output" : out.replace("\n", " ").strip()}
                output_trace["traces"].append(trace_data)
                #print(process[k].communicate())
                process[k] = None
        k += 1
    if (fut <= 0):
        ures = True

with open("traceroute.json", "w") as outfile:  
    json.dump(output_trace, outfile, indent = 1)

