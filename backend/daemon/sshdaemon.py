import happybase
import sys
import time
import os
from daemon import Daemon
import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException


class MyDaemon(Daemon):
    def run(self):
        # All input is read from an input file
        # Format of the file is specified in the file itself
        inputfile = open(os.path.join(sys.path[0], '../input.txt'), 'r')

        ips = list()
        unames = list()
        pwds = list()

        for i, line in enumerate(inputfile):
            if i == 5:  # Line 6 contains update frequency for the data
                updatefreq = int(line)
            elif i == 6:  # Line 7 contais timeout
                timeout = line
            elif i >= 8 and i % 5 == 3:  # Each line with lineno%4==1 contains an IP address
                ips.append(line.strip())
            elif i >= 8 and i % 5 == 0:  # Each line with lineno%4==1 contains corresponding username for SSH
                unames.append(line.strip())
            elif i >= 8 and i % 5 == 1:  # Each line with lineno%4==1 contains corresponding password for SSH
                pwds.append(line.strip())

        inputfile.close()

        # Initialising SSH and HBase connection
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('ssh')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        while True:
            if ips:
                # ssh = paramiko.SSHClient()
                # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                sshresults = dict()  # Stores SSH output

                for i in range(len(ips)):
                    try:
                        ssh.connect(ips[i], username=unames[i],
                                    password=pwds[i], timeout=int(timeout))
                        sshresults[ips[i]+':ssh'] = 'True'
                        sshresults[ips[i]+':last'] = ""

                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                            "last -n 10")

                        for j in ssh_stdout:
                            j = j.split(" ")
                            if j[0] != "" and j[0] != "wtmp" and j[0] != "reboot":
                                
                                sshresults[ips[i]+':last'] += (j[0]+"\n")

                    except (BadHostKeyException, AuthenticationException,
                            SSHException) as e:
                        sshresults[ips[i]+':ssh'] = 'False: ' + e
                        sshresults[ips[i]+":last"] = "Could not SSH"

                # Writes to database after deleting previous value
                # Key = 'row', value = sshresults
                conn.open()
                table.delete('row')
                table.put('row', sshresults)
                conn.close()

                # Delay
                time.sleep(updatefreq)
            else:
                print('No input specified')
                sys.exit()


if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon3.pid', stderr=os.path.join(
        sys.path[0], 'dumps/ssherrors.txt'), stdout=os.path.join(sys.path[0], 'dumps/sshoutput.txt'))
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
