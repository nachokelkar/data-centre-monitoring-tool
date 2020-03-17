import sys, time
from daemon import Daemon
from datetime import datetime
import ecks

class MyDaemon(Daemon):
        def run(self):
            # All input is read from an input file
            # Format of the file is specified in the file itself
            inputfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/input.txt", "r")
            
            ips = list()
            
            for i, line in enumerate(inputfile):
                if i==5: # Line 6 contains update frequency for the data
                    updatefreq = int(line)
                elif i==6: # Line 7 contais timeout 
                    timeout = int(line)
                elif i>=8 and i%4==0: # Each line with lineno%4==1 contains an IP address
                    ips.append(line.strip())

            e = ecks.Ecks()
            
            # Initialises an empty file
            # Comment all lines to allow appending of data on each run of the daemon, instead of starting with an empty file on each run
            # Files: cpudata.txt, memdata.txt, uptdata.txt, dskdata.txt
            cpufile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/cpudata.txt", "w")
            memfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/memdata.txt", "w")
            uptfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/uptdata.txt", "w")
            dskfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/dskdata.txt", "w")
            cpufile.write("")
            memfile.write("")
            uptfile.write("")
            dskfile.write("")
            cpufile.close()
            memfile.close()
            uptfile.close()
            dskfile.close()

            while True:
                if ips:
                    for i in ips:
                        # Getting data using Ecks
                        # Usage: e.get_data("ip address", "group", "data type")
                        cpu_data = e.get_data(i, "public", "cpu") # cpu_data is a tuple of the form (user%, cpu%, idle%)
                        mem_data = e.get_data(i, "public", "memory") # mem_data is a tuple of the form (total_swap, avail_swap, total_real, avail_real, mem_buffer, mem_cached) in kB
                        upt_data = e.get_data(i, "public", "uptime") # upt_data is uptime in seconds
                        dsk_data = e.get_data(i, "public", "disk") # dsk_data is a list of tuples of the form (type, path, size in bytes, used bytes) for each block device

                        # Writing data to each file
                        cpufile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/cpudata.txt", "a+")
                        memfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/memdata.txt", "a+")
                        uptfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/uptdata.txt", "a+")
                        dskfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/dskdata.txt", "a+")
                        cpufile.write("[" +str(datetime.now()) +"]\t" +i +"\t" +str(cpu_data) +"\n")
                        memfile.write("[" +str(datetime.now()) +"]\t" +i +"\t" +str(mem_data) +"\n")
                        uptfile.write("[" +str(datetime.now()) +"]\t" +i +"\t" +str(upt_data) +"\n")
                        dskfile.write("[" +str(datetime.now()) +"]\t" +i +"\t" +str(dsk_data) +"\n")
                        cpufile.close()
                        memfile.close()
                        uptfile.close()
                        dskfile.close()
                
                    # Delay
                    time.sleep(updatefreq)
                else:
                    print("No input specified")
                    sys.exit()
 
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon1.pid', stderr="/home/pranav/Work/MiniProject/data-centre-monitoring-tool/dumps/snmperrors.txt", stdout="/home/pranav/Work/MiniProject/data-centre-monitoring-tool/dumps/snmpoutput.txt")
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)