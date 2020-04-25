#!/bin/bash

if [ "$1" = "start" ]
then
    sudo rm -rf dumps
    sudo mkdir dumps
    sudo python2 backend/daemon/snmpdaemon.py start
    echo 'SNMP daemon RUNNING'
    sudo python2 backend/daemon/pingdaemon.py start
    echo 'Ping daemon RUNNING'
    sudo python2 backend/daemon/sshdaemon.py start
    echo 'SSH daemon RUNNING'
elif [ "$1" = "stop" ]
then
    sudo python2 backend/daemon/snmpdaemon.py stop
    echo 'SNMP daemon STOPPED'
    sudo python2 backend/daemon/pingdaemon.py stop
    echo 'Ping daemon STOPPED'
    sudo python2 backend/daemon/sshdaemon.py stop
    echo 'SSH daemon STOPPED'
elif [ "$1" = "restart" ]
then
    sudo python2 backend/daemon/snmpdaemon.py restart
    echo 'SNMP daemon RESTARTED'
    sudo python2 backend/daemon/pingdaemon.py restart
    echo 'Ping daemon RESTARTED'
    sudo python2 backend/daemon/sshdaemon.py restart
    echo 'SSH daemon RESTARTED'
else
    echo 'Usage: ./dcmt.sh [start|stop|restart]'
fi