# Data Centre Monitoring Tool
A basic tool to monitor networks and servers in a data centre

## What it does (as of now)
- Pings IP addresses
- Checks and stores CPU data

## Usage
- Set IP addresses in ips.txt
- To start daemon processes,\
  `$ ./daemon.sh start`
- To stop daemon processes,\
  `$ ./daemon.sh stop`
- To restart daemon processes,\
  `$ ./daemon.sh restart`
- To start flask app,\
  `$ python flaskapp.py`
- Output data stored in `ping.txt`, `snmp.txt`
- Daemon output and errors stored in `/dumps`

> ### Note on daemon files
> Change pidfile, output, error file paths for every new daemon python created.\
  This is done by changing the first parameter passed in the constructor function in `__main__`

### To-do
- Make update frequency a changing argument (and not hardcoded)
- SSH check
- Topology display
- Front-end
