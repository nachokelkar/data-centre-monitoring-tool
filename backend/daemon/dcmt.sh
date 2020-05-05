#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ "$1" = "start" ]
then
    if [ $# -eq 4 ]
    then
        echo 'Removing previous dumps files'
        sudo rm -rf $DIR/dumps
        echo 'Creating dumps folder'
        sudo mkdir $DIR/dumps
        sudo python2 $DIR/snmpdaemon.py start $2 $4
        sudo python2 $DIR/pingdaemon.py start $2 $3
        sudo python2 $DIR/sshdaemon.py start $2 $3
    else
        echo 'Usage: ./dcmt.sh start [timeout] [update freq for ping and ssh] [update freq for snmp]'
    fi
elif [ "$1" = "stop" ]
then
    sudo python2 $DIR/snmpdaemon.py stop
    sudo python2 $DIR/pingdaemon.py stop
    sudo python2 $DIR/sshdaemon.py stop
elif [ "$1" = "restart" ]
then
    sudo python2 $DIR/snmpdaemon.py restart
    echo 'SNMP daemon RESTARTED'
    sudo python2 $DIR/pingdaemon.py restart
    echo 'Ping daemon RESTARTED'
    sudo python2 $DIR/sshdaemon.py restart
    echo 'SSH daemon RESTARTED'
else
    echo 'Usage: ./dcmt.sh [start|stop|restart] [start:timeout] [start:update freq for ping and ssh] [start:update freq for snmp]'
fi