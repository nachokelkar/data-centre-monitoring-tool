# Data Centre Monitoring Tool
A basic tool to monitor the network and servers in a data centre.

## What it does (as of now)
* Pings IP addresses
* Tests if SSH is working with the given username and password
* Checks and stores CPU data
* Checks and stores memory utilisation
* Checks and stores disk utilisation
* Checks and stores uptime
* Finds last 5 logged in users

## Initial setup for inputs
* Inputs must be in `backend/inputs.xlsx`
* Column names "IP", "Rack_number", "Username", "Password" must not be changed.
* "IP" should *always* be the first column
* Make sure there are absolutely no errors in the addresses.\
We have done as much error handling as possible, there might be unhandled cases.



---
## Backend
```sh
$ cd backend
```


### Initial setup for database
HBase must be installed (https://hbase.apache.org/book.html#quickstart).\
To initialise the tables
```sh
$ python util/table_init.py
```
To clear the tables
```sh
$ python util/table_clr.py
```
The application does not initialise or clear tables by itself.\
Before running, make sure tables are initialised.

### Usage
* Create input file `input.txt` as above
* Make sure HBase is running\
(In HBase folder, `$ bin/start-hbase.sh`)
* Thrift must be running on port 9090\
(In HBase folder, `$ bin/hbase-daemon.sh start thrift -p 9090`)
* To start daemon processes,
  ```sh
  $ daemon/dcmt.sh start [timeout] [ping and ssh update freq] [snmp update freq]
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



---
## Frontend
```sh
$ cd frontend
```

### To run 
```sh
$ yarn
$ yarn start
```
---



### To-do
* Last logged in (user, time)
* Users on the systems (other than root)
* Ansible (low priority)
* Check out front-end
* Check switch, router health (1)
* Display log files (head, tail, entire file)