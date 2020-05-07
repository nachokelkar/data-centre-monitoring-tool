import happybase
import sys
import time
import os
from daemon import Daemon


class MyDaemon(Daemon):
    def run(self):
        # Initialising HBase connection
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('ping')

        while True:
            if self.inputdata["IP"]:  # Run only if there are IP addresses in the file
                pingresults = dict()  # Stores results of the ping test

                for i in range(len(self.inputdata["IP"])):
                    # Running ping command
                    # response will hold 0 if successful, something else if it fails
                    pingresponse = os.system('ping -c 1 -w ' +str(self.timeout) + ' ' + self.inputdata["IP"][i])
                    
                    # Adds result to the ping command
                    pingresults[self.inputdata["IP"][i].strip()+":ping"] = str(pingresponse == 0)

                # Deleting previous output, putting new output into the database
                # Key = 'row', Value = 'pingresults'
                conn.open()
                table.delete('row')
                table.put('row', pingresults)
                conn.close()

                # Delay
                time.sleep(self.upfreqping)

            else:  # If no input is detected
                print('No input detected')
                sys.exit()


if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon2.pid', stderr=os.path.join(sys.path[0], 'dumps/pingerrors.txt'), stdout=os.path.join(sys.path[0], 'dumps/pingoutput.txt'))
    if len(sys.argv) == 4 or len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("Starting ping daemon")
            daemon.start(timeout=sys.argv[2], upfreqping=sys.argv[3])
        elif 'stop' == sys.argv[1]:
            print("Stopping ping daemon")
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
