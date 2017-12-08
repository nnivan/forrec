#!/bin/bash

DIR="$1"

apt-get update
apt-get install -y python-pip
cd $DIR
pip install -r requirements.txt
pip install -e .
