# Garage Controller
A DIY project for an automatic garage door closer using a raspberry pi zero w, a reed switch magnetic sensor, and a 5v relay module.

## File list:

### garageCloser.py
Contains code logic for running the garage door closer. It will automatically trigger the relay to close the garage door after detecting 5 minutes of the garage door being open through the reed switch magnetic sensor. 

This file creates a logger text file to log every time the program is run. This is meant to be used for troubleshooting when was the last reboot of the raspberry pi.

### loggerGarage.txt
This is the file created by the garageCloser.py to track the reboots of the raspberry pi and consequently track every time the program has re-launched.

### launcher.sh
Deprecated. This file is not in use as of the latest commit of this readme. It was originally meant to be used as a launcher script for a crontab that would run every time the raspberry pi boots. This prooved to be unreliable, so this functionality moved to rc.local

## General notes and autolaunch
For everything to run correctly, copy the latest files from the garageControl folder of this repository into the desktop of your pi. Then modify your rc.local as described below.

This program is meant to automatically launch even in headless mode every time the pi boots up. To accomplish this, a line was added to the file /etc/rc.local with the following:
```
sudo python /home/pi/Desktop/garageControl/garageCloser.py &
sleep 30
sudo python /home/pi/Desktop/garageControl/imapEmailMonitorHtml.py &
```
