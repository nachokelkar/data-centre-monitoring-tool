import ecks, time
from datetime import datetime

data = open("diskdata.txt", "w")
data.write("")
data.close()

ips = ["127.0.0.1"]
updatefreq = 5
looper = True
e = ecks.Ecks()

while(looper):
    data = open("diskdata.txt", "a")
    for i in ips:
        cpu_data = e.get_data(i, "public", "cpu")
        data.write("[" +str(datetime.now()) +"]\t" +i +"\t" +str(cpu_data) +"\n")
        print("Log entry - " +str(datetime.now()))
    data.close()
    time.sleep(updatefreq)