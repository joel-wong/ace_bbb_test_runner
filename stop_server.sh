#!/bin/sh
result=$(pgrep python3)
if [ -z "$result" ]; then
	echo "No Server Running"
else
	kill -s INT $result
fi
echo "Server Stopped"
exit
