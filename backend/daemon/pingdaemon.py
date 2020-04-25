import happybase
import sys
import time
import os
from daemon import Daemon
import happybase


class MyDaemon(Daemon):
    def run(self):
        # All input is read from an input file
        # Format of the file is specified in the file itself
        inputfile = open(os.path.join(sys.path[0], '../input.txt'), 'r')

        ips = list()  # Stores list of IP addresses

        for i, line in enumerate(inputfile):
            # i = lineno - 1
            if i == 5:  # Line 6 contains update frequency for the data
                updatefreq = int(line.strip())
            elif i == 6:  # Line 7 contains timeout for the ping
                # Timeout is set as a string and not converted to an int because it isn't required
                timeout = line.strip()
            elif i >= 8 and i % 5 == 3:  # Each line with lineno%5==4 contains an IP address
                # Stripping is done to remove trailing newlines
                ips.append(line.strip())
                
        inputfile.close()

        # Initialising HBase connection
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('ping')

        while True:
            if ips:  # Run only if there are IP addresses in the file
                pingresults = dict()  # Stores results of the ping test

                for i in ips:
                    # Running ping command
                    # response will hold 0 if successful, something else if it fails
                    pingresponse = os.system('ping -c 1 -w ' + timeout + ' ' + i)
                    
                    # Adds result to the ping command
                    pingresults[i.strip()+":ping"] = str(pingresponse == 0)

                # Deleting previous output, putting new output into the database
                # Key = 'row', Value = 'pingresults'
                conn.open()
                table.delete('row')
                table.put('row', pingresults)
                conn.close()

                # Delay
                time.sleep(updatefreq)

            else:  # If no input is detected
                print('No input detected')
                sys.exit()


if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon2.pid', stderr=os.path.join(sys.path[0], 'dumps/pingerrors.txt'), stdout=os.path.join(sys.path[0], 'dumps/pingoutput.txt'))
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('Unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        print('usage: %s start|stop|restart' % sys.argv[0])
        sys.exit(2)
