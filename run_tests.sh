#!/bin/bash

set -euo pipefail
IFS=$'\n\t'


function ephymeral_port(){
    LPORT=32768;
    UPORT=60999;
    while true; do
        MPORT=$(($LPORT + ($RANDOM % $UPORT)));
        (echo "" >/dev/tcp/127.0.0.1/${MPORT}) >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo $MPORT;
            return 0;
        fi
    done
}

function finish {
    docker kill mongo-test
}



my_port=$(ephymeral_port)

echo $my_port

docker run -d --rm --name mongo-test -p $my_port:27017 mongo:3.4
trap finish EXIT

until mongo --quiet --port $my_port --eval 'db.isMaster().ismaster'
do
  echo "Waiting for mongo to launch"
  sleep 2
done

echo "We launched mongo!"
pytest --mongo-port $my_port

