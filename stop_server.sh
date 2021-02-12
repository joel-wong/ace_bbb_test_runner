#!/bin/sh
result=$(pgrep python3)
if [ -z "$result" ]; then
	echo "No Server Running"
else
	kill -2 $result
fi
exit
