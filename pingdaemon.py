import sys, time
from daemon import Daemon
from datetime import datetime
import os

class MyDaemon(Daemon):
        def run(self):
            # All input is read from an input file
            # Format of the file is specified in the file itself
            inputfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/input.txt", "r")
            
            ips = list() # Stores list of IP addresses

            for i, line in enumerate(inputfile):
                # i = lineno - 1
                if i==5: # Line 6 contains update frequency for the data
                    updatefreq = int(line.strip())
                elif i==6: # Line 7 contains timeout for the ping
                    timeout = line.strip() # Timeout is set as a string and not converted to an int because it isn't required
                elif i>=8 and i%4==0: # Each line with lineno%4==1 contains an IP address
                    ips.append(line.strip()) # Stripping is done to remove trailing newlines

            while True:
                if ips: # Run only if there are IP addresses in the file
                    pingresults = list() # Stores results of the ping test

                    for i in ips:
                        # Running ping command
                        # response will hold 0 if successful, something else if it fails
                        response = os.system("ping -c 1 -w " +timeout +" " +i)
                        pingresults.append(i.strip() +"\t" +str(response == 0) +"\n")
                    
                    # Writing results of ping to a file
                    pingfile = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/ping.txt", "w")
                    for result in pingresults:
                        pingfile.write(result)
                    pingfile.close()

                    # Delay
                    time.sleep(updatefreq)
                
                else: # If no input is detected
                    print("No input detected")
                    sys.exit()
 
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
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)