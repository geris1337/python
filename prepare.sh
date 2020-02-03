#!/bin/sh
sudo apt update  
sudo apt install firefox firefox-geckodriver python3 python3-pip -y
pip3 install -U pytest selenium
