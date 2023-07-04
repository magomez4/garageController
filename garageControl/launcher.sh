#!/bin/sh
#launcher.sh
#navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Desktop/garageControl
sudo python garageCloser.py
cd /
