#!/bin/bash

DIR="$1"

#apt-get update
#apt-get install -y python-pip
cd $DIR
pip3 install -r requirements.txt
pip3 install -e .
