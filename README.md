# SySMon – System Monitor

SySMon is a simple web dashboard for monitoring a Linux server.
It collects CPU, RAM, uptime and logs, stores them in MySQL, 
and shows graphs via Chart.js.

## Features
- CPU & RAM usage graph (last 24 records)
- Uptime and logs
- Flask + Bootstrap + Chart.js

## installation
```bash
git clone https://github.com/yourname/SysMon.git
cd SysMon
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
