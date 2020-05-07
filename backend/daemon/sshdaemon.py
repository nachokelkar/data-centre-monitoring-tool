import happybase
import sys
import time
import os
from daemon import Daemon
import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException


class MyDaemon(Daemon):
    def run(self):

        # Initialising SSH and HBase connection
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('ssh')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        while True:
            if self.inputdata["IP"]:
                sshresults = dict()  # Stores SSH output

                for i in range(len(self.inputdata["IP"])):
                    # Try SSH connection
                    try:
                        ssh.connect(self.inputdata["IP"][i], username=self.inputdata["Username"][i],
                                    password=self.inputdata["Password"][i], timeout=int(self.timeout))
                        sshresults[self.inputdata["IP"][i]+':ssh'] = 'True'
                        sshresults[self.inputdata["IP"][i]+':last'] = ""

                        # This runs the "last" command on the target system, to find last 5 users
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                            "last -n 10")
                        # This part is used to format the output of "last"
                        for j in ssh_stdout:
                            j = j.split(" ")
                            if j[0] != "" and j[0] != "wtmp" and j[0] != "reboot":
                                sshresults[self.inputdata["IP"]
                                           [i]+':last'] += (j[0]+"\n")

                    # Show exception on failure
                    except (BadHostKeyException, AuthenticationException,
                            SSHException) as e:
                        sshresults[self.inputdata["IP"]
                                   [i]+':ssh'] = 'False: ' + str(e)
                        sshresults[self.inputdata["IP"]
                                   [i]+":last"] = "Could not SSH"

                # Writes to database after deleting previous value
                # Key = 'row', value = sshresults
                conn.open()
                table.delete('row')
                table.put('row', sshresults)
                conn.close()

                # Delay
                time.sleep(self.upfreqping)
            else:
                print('No input specified')
                sys.exit()


if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon3.pid', stderr=os.path.join(
        sys.path[0], 'dumps/ssherrors.txt'), stdout=os.path.join(sys.path[0], 'dumps/sshoutput.txt'))
    if len(sys.argv) == 4 or len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("Starting SSH daemon")
            daemon.start(timeout=sys.argv[2], upfreqping=sys.argv[3])
        elif 'stop' == sys.argv[1]:
            print("Stopping SSH daemon")
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
