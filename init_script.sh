#!/bin/bash
apt-get install python -y
cd honeynode
python get-pip.py
pip install paramiko
pip install pyinotify
pip install geoip2
pip install python-daemon
sed -i 's/Port 22/Port 2222/g' /etc/ssh/sshd_config
service ssh restart
