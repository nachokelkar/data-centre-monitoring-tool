import sys, time
from daemon import Daemon
from datetime import datetime
import ecks
 
class MyDaemon(Daemon):
        def run(self):
            ips = ["127.0.0.1"]
            updatefreq = 2
            e = ecks.Ecks()
            f = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/output.txt", "w")
            f.write("")
            while True:            
                for i in ips:
                    cpu_data = e.get_data(i, "public", "cpu")
                    f = open("/home/pranav/Work/MiniProject/data-centre-monitoring-tool/output.txt", "a+")
                    f.write("[" +str(datetime.now()) +"]\t" +i +"\t" +str(cpu_data) +"\n")
                time.sleep(updatefreq)
                f.close()
 
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid', stderr="/home/pranav/Work/MiniProject/data-centre-monitoring-tool/errors.txt", stdout="/home/pranav/Work/MiniProject/data-centre-monitoring-tool/output.txt")
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