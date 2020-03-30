#!/bin/sh
git branch bak || true
while true
do
	touch canary
	rm -f stop
	PYTHONUNBUFFERED=1 python3 main.py 2>&1 | tee -a cybersocbot.log
	if [ -e canary ]
	then
		python3 fallback.py
	fi
	if [ -e stop ]
	then
		exit 0
	fi
done
