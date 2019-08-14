#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
nohup mkdocs serve -a 127.0.0.1:8081 >> /root/docs-manager/logs/font.log &
cd /root/docs-manager/backend/
nohup python3 start.py >> /root/docs-manager/logs/back.log &
service nginx restart
tail -f /root/docs-manager/logs/font.log
