import sys, time
from daemon import Daemon
from datetime import datetime
import os
 
class MyDaemon(Daemon):
        def run(self):
            # Read IP addresses from ips.txt
            ipfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/ips.txt", "r")
            ips = ipfile.readlines()
            ipfile.close()

            # Enter refresh period here
            updatefreq = 5

            while True:
                pingfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/ping.txt", "w")
                
                # Set max allowed timeout here
                timeout = 10

                for i in ips:
                    # Running ping command
                    # response will hold 0 if successful
                    response = os.system("ping -n 1 -w 10 " +i)
                    pingfile.write(i +"\t" +str(response == 0) +"\n")
                
                pingfile.close()

                # Delay
                time.sleep(updatefreq)
 
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon2.pid', stderr="/home/pranav/Work/MiniProject/data-centre-monitoring-tool/dumps/pingerrors.txt", stdout="/home/pranav/Work/MiniProject/data-centre-monitoring-tool/dumps/pingoutput.txt")
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