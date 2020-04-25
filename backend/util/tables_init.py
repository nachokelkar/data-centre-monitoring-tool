import happybase
import os
import sys

conn = happybase.Connection('localhost', port=9090)
inputfile = open(os.path.join(sys.path[0], '../input.txt'), 'r')

ips = dict()

for i, line in enumerate(inputfile):
    if i >= 8 and i % 4 == 0:  # Each line with lineno%4==1 contains an IP address
        ips[line.strip()] = dict()

conn.open()
conn.create_table('snmp', ips)
conn.create_table('ping', ips)
conn.create_table('ssh', ips)
conn.close()

conn.open()
print("TABLES CREATED: ", conn.tables())
conn.close()