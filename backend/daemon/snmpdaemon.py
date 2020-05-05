import happybase
import sys
import time
import os
from daemon import Daemon
from datetime import datetime
import ecks


class MyDaemon(Daemon):
    def run(self):
        # Initialising SNMP and HBase connections
        e = ecks.Ecks() # SNMP using Ecks
        conn = happybase.Connection('localhost', port=9090) # HBase using happybase, connecting to Thrift port 9090
        table = conn.table('snmp') # Setting the table used

        while True:
            if self.inputdata["IP"]:
                putdict = dict()  # Stores the data that is to be put into the database

                for i in range(len(self.inputdata["IP"])):
                    try:
                        # Getting data using Ecks
                        # Usage: e.get_data('ip address', 'snmp group', 'data type')
                        # cpu_data is a tuple of the form (user%, cpu%, idle%)
                        cpu_data = e.get_data(self.inputdata["IP"][i], 'public', 'cpu')
                        # mem_data is a tuple of the form (total_swap, avail_swap, total_real, avail_real, mem_buffer, mem_cached) in kB
                        mem_data = e.get_data(self.inputdata["IP"][i], 'public', 'memory')
                        # upt_data is uptime in seconds
                        upt_data = e.get_data(self.inputdata["IP"][i], 'public', 'uptime')
                        # dsk_data is a list of tuples of the form (type, path, size in bytes, used bytes) for each block device
                        dsk_data = e.get_data(self.inputdata["IP"][i], 'public', 'disk')
                        # os_data returns the host operating system info
                        os_data = e.get_data(self.inputdata["IP"][i], 'public', 'os')

                        # Preparing the data for putting into the database
                        putdict[self.inputdata["IP"][i]+':cpu'] = str(cpu_data)
                        putdict[self.inputdata["IP"][i]+':memory'] = str(mem_data)
                        putdict[self.inputdata["IP"][i]+':disk'] = str(dsk_data)
                        putdict[self.inputdata["IP"][i]+':upt'] = str(upt_data)
                        putdict[self.inputdata["IP"][i]+':os'] = str(os_data)
                        putdict[self.inputdata["IP"][i]+':rack'] = str(self.inputdata["Rack_number"][i])
                    except Exception as e:
                        putdict[self.inputdata["IP"][i]+':cpu'] = "FAILED:" +str(e)
                        putdict[self.inputdata["IP"][i]+':memory'] = "FAILED:" +str(e)
                        putdict[self.inputdata["IP"][i]+':disk'] = "FAILED:" +str(e)
                        putdict[self.inputdata["IP"][i]+':upt'] = "FAILED:" +str(e)
                        putdict[self.inputdata["IP"][i]+':os'] = "FAILED:" +str(e)
                        putdict[self.inputdata["IP"][i]+':rack'] = str(self.inputdata["Rack_number"][i])

                # Writing to database
                # Key = timestamp during write
                conn.open()
                table.put(str(datetime.now()), putdict)
                conn.close()

                # Delay
                time.sleep(self.upfreqsnmp)
            else:
                print('No input specified')
                sys.exit()


if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon1.pid', stderr=os.path.join(
        sys.path[0], 'dumps/snmperrors.txt'), stdout=os.path.join(sys.path[0], 'dumps/snmpoutput.txt'))
    if len(sys.argv) == 4 or len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("Starting SNMP daemon")
            daemon.start(timeout=sys.argv[2], upfreqsnmp=sys.argv[3])
        elif 'stop' == sys.argv[1]:
            print("Stopping SNMP daemon")
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
