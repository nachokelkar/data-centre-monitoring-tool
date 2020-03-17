# Data Centre Monitoring Tool
A basic tool to monitor the network and servers in a data centre.

## What it does (as of now)
* Pings IP addresses
* Tests if SSH is working with the given username and password
* Checks and stores CPU data
* Checks and stores memory utilisation
* Checks and stores disk utilisation
* Checks and stores uptime

## Initial setup for inputs
Inputs must be in `inputs.txt` in the following format:
* Frequency of updates (in seconds) must be on Line 6
* Allowed timeout for pinging and SSH (in seconds) must be on Line 7
* IP addresses and other details must be in the following format starting on Line 8:
  * IP address on the first line
  * SSH username on the second line
  * SSH password on the third line
  * Empty line

## Usage
* Create input file `input.txt` as above
* To start daemon processes,\
  `$ ./daemon.sh start`
* To stop daemon processes,\
  `$ ./daemon.sh stop`
* To restart daemon processes,\
  `$ ./daemon.sh restart`
* To start flask app,\
  `$ python flaskapp.py`
* Outputs are stored as following:
  * Ping check stored in `ping.txt` as `[IP address]\t[True|False]`
  * SSH check stored in `ssh.txt` as `[IP address]\t[True|False]`
  * CPU data stored in `cpudata.txt` as `[Timestamp]\t[IP address]\t[CPU Utilisation]`
  * Memory data stored in `cpudata.txt` as `[Timestamp]\t[IP address]\t[Memory Utilisation]`
  * Disk data stored in `cpudata.txt` as `[Timestamp]\t[IP address]\t[Disk Utilisation]`
  * Uptime data stored in `cpudata.txt` as `[Timestamp]\t[IP address]\t[Uptime]`
* Daemon output and errors stored in `/dumps`

> ### Note on daemon files
> Change pidfile, output, error file paths for every new daemon python created.\
  This is done by changing the first parameter passed in the constructor function in `__main__`

### To-do
- Topology display
- Last logged in user
- Total users on the system
- Front-end
