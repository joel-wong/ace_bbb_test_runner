#!/bin/sh
result=$(pgrep python)
if [ -z "$result" ]; then
	echo "No Server Running"
else
	kill $result
fi
exit
