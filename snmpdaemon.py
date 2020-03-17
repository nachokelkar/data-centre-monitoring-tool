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

        ips = list()

        for i, line in enumerate(inputfile):
            if i == 5:  # Line 6 contains update frequency for the data
                updatefreq = int(line)
            elif i == 6:  # Line 7 contais timeout
                timeout = int(line)
            elif i >= 8 and i % 4 == 0:  # Each line with lineno%4==1 contains an IP address
                ips.append(line.strip())

        e = ecks.Ecks()

        # Initialises an empty file
        # Comment all lines to allow appending of data on each run of the daemon, instead of starting with an empty file on each run
        # Files: cpudata.txt, memdata.txt, uptdata.txt, dskdata.txt
        cpufile = open(os.path.join(sys.path[0], 'cpudata.txt'), 'w')
        memfile = open(os.path.join(sys.path[0], 'memdata.txt'), 'w')
        uptfile = open(os.path.join(sys.path[0], 'uptdata.txt'), 'w')
        dskfile = open(os.path.join(sys.path[0], 'dskdata.txt'), 'w')
        cpufile.write('')
        memfile.write('')
        uptfile.write('')
        dskfile.write('')
        cpufile.close()
        memfile.close()
        uptfile.close()
        dskfile.close()

        while True:
            if ips:
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

                    # Writing data to each file
                    cpufile = open(os.path.join(
                        sys.path[0], 'cpudata.txt'), 'a+')
                    memfile = open(os.path.join(
                        sys.path[0], 'memdata.txt'), 'a+')
                    uptfile = open(os.path.join(
                        sys.path[0], 'uptdata.txt'), 'a+')
                    dskfile = open(os.path.join(
                        sys.path[0], 'dskdata.txt'), 'a+')
                    cpufile.write('[' + str(datetime.now()) +
                                  ']\t' + i + '\t' + str(cpu_data) + '\n')
                    memfile.write('[' + str(datetime.now()) +
                                  ']\t' + i + '\t' + str(mem_data) + '\n')
                    uptfile.write('[' + str(datetime.now()) +
                                  ']\t' + i + '\t' + str(upt_data) + '\n')
                    dskfile.write('[' + str(datetime.now()) +
                                  ']\t' + i + '\t' + str(dsk_data) + '\n')
                    cpufile.close()
                    memfile.close()
                    uptfile.close()
                    dskfile.close()

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
