import happybase
import sys
import time
import os
from daemon import Daemon
from datetime import datetime
import ecks


class MyDaemon(Daemon):
    def run(self):
        # All input is read from an input file
        # Format of the file is specified in the file itself
        inputfile = open(os.path.join(sys.path[0], 'input.txt'), 'r')

        ips = list()  # Stores the IP addresses given in the input

        for i, line in enumerate(inputfile):
            if i == 5:  # Line 6 contains update frequency for the data
                updatefreq = int(line)
            elif i >= 8 and i % 4 == 0:  # Each line with lineno%4==1 contains an IP address
                ips.append(line.strip())

        inputfile.close()

        # Initialising SNMP and HBase connections
        e = ecks.Ecks()
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('snmp')

        while True:
            if ips:
                putdict = dict()  # Stores the data that is to be put into the database

                for i in ips:
                    # Getting data using Ecks
                    # Usage: e.get_data('ip address', 'group', 'data type')
                    # cpu_data is a tuple of the form (user%, cpu%, idle%)
                    cpu_data = e.get_data(i, 'public', 'cpu')
                    # mem_data is a tuple of the form (total_swap, avail_swap, total_real, avail_real, mem_buffer, mem_cached) in kB
                    mem_data = e.get_data(i, 'public', 'memory')
                    # upt_data is uptime in seconds
                    upt_data = e.get_data(i, 'public', 'uptime')
                    # dsk_data is a list of tuples of the form (type, path, size in bytes, used bytes) for each block device
                    dsk_data = e.get_data(i, 'public', 'disk')
                    # os_data returns the host operating system info
                    os_data = e.get_data(i, 'public', 'os')

                    # Preparing the data for putting into the database
                    putdict[i+':cpu'] = str(cpu_data)
                    putdict[i+':memory'] = str(mem_data)
                    putdict[i+':disk'] = str(dsk_data)
                    putdict[i+':upt'] = str(upt_data)
                    putdict[i+':os'] = str(os_data)

                # Writing to database
                # Key = timestamp during write
                conn.open()
                table.put(str(datetime.now()), putdict)
                conn.close()

                # Delay
                time.sleep(updatefreq)
            else:
                print('No input specified')
                sys.exit()


if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon1.pid', stderr=os.path.join(
        sys.path[0], 'dumps/snmperrors.txt'), stdout=os.path.join(sys.path[0], 'dumps/snmpoutput.txt'))
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
