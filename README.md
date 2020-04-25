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
Inputs must be in `backend/inputs.txt` in the following format:
* Frequency of updates (in seconds) must be on Line 6
* Allowed timeout for pinging and SSH (in seconds) must be on Line 7
* IP addresses and other details must be in the following format starting on Line 8:
  * IP address on the first line
  * SSH username on the second line
  * SSH password on the third line
  * Empty line

---
## Backend
```sh
cd backend
```


### Initial setup for database
The database must be set up according to the IP addresses.\
HBase must be installed (https://hbase.apache.org/book.html#quickstart).\
To initialise the tables
```sh
$ python util/table_init.py
```
To clear the tables
```sh
$ python util/table_clr.py
```
Once that is done, run `util/table_init.py` to create the tables and `util/table_clr.py` to delete tables.

### Usage
* Create input file `input.txt` as above
* Make sure HBase is running\
(In HBase folder, `$ bin/start-hbase.sh`)
* Thrift must be running on port 9090\
(In HBase folder, `$ bin/hbase-daemon.sh start thrift -p 9090`)
* To start daemon processes,
  ```sh
  $ daemon/dcmt.sh start
  ```
* To stop daemon processes,
  ```sh
  $ daemon/dcmt.sh stop
  ```
* To restart daemon processes,
  ```sh
  $ daemon/dcmt.sh restart
  ```
* To start flask app,
  ```sh
  $ python flaskapp.py
  ```
* Outputs are stored as in tables `'snmp'`, `'ping'` and `'ssh'` in HBase
* Daemon output and errors stored in `daemon/dumps`

> ### Note on daemon files
> Change pidfile, output, error file paths for every new daemon python created.\
  This is done by changing the first parameter passed in the constructor function in `__main__`

### To-do
* Last logged in (user, time)
* Users on the systems (other than root)
* Ansible (low priority)
* Check out front-end
* Check switch, router health (1)
* Display log files (head, tail, entire file)
---
## Frontend

### To run 
```sh
$ yarn
$ yarn start
```


