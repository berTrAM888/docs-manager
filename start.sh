#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
nohup mkdocs serve -a 127.0.0.1:8081 >> logs/font.log &
cd backend/
nohup python3 start.py >> ../logs/back.log &
