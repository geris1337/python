#!/bin/sh
sudo apt update  
sudo apt install wget python3 python3-pip firefox-esr -y
sudo apt install firefox -y
pip3 install -U pytest selenium
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xvzf geckodriver-v0.26.0-linux64.tar.gz
rm geckodriver-v0.26.0-linux64.tar.gz
chmod +x geckodriver
sudo cp geckodriver /usr/local/bin/
