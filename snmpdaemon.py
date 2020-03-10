import sys, time
from daemon import Daemon
from datetime import datetime
import ecks
 
class MyDaemon(Daemon):
        def run(self):
            # Read IP addresses from ips.txt
            ipfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/ips.txt", "r")
            ips = ipfile.readlines()
            ipfile.close()

            # Enter refresh period here
            updatefreq = 5

            e = ecks.Ecks()
            
            # Initialises an empty file
            cpufile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/snmp.txt", "w")
            cpufile.write("")
            cpufile.close()

            while True:            
                for i in ips:
                    # Getting CPU data
                    cpu_data = e.get_data(i, "public", "cpu")

                    # Writing CPU data
                    cpufile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/snmp.txt", "a+")
                    cpufile.write("[" +str(datetime.now()) +"]\t" +i +"\t" +str(cpu_data) +"\n")
                    cpufile.close()
                
                # Delay
                time.sleep(updatefreq)
 
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