#!/bin/bash

if [ "$1" = "start" ]
then
    sudo rm -rf dumps
    sudo mkdir dumps
    sudo python2 daemon/snmpdaemon.py start
    echo 'SNMP daemon RUNNING'
    sudo python2 daemon/pingdaemon.py start
    echo 'Ping daemon RUNNING'
    sudo python2 daemon/sshdaemon.py start
    echo 'SSH daemon RUNNING'
elif [ "$1" = "stop" ]
then
    sudo python2 daemon/snmpdaemon.py stop
    echo 'SNMP daemon STOPPED'
    sudo python2 daemon/pingdaemon.py stop
    echo 'Ping daemon STOPPED'
    sudo python2 daemon/sshdaemon.py stop
    echo 'SSH daemon STOPPED'
elif [ "$1" = "restart" ]
then
    sudo python2 daemon/snmpdaemon.py restart
    echo 'SNMP daemon RESTARTED'
    sudo python2 daemon/pingdaemon.py restart
    echo 'Ping daemon RESTARTED'
    sudo python2 daemon/sshdaemon.py restart
    echo 'SSH daemon RESTARTED'
else
    echo 'Usage: ./dcmt.sh [start|stop|restart]'
fi