#!/bin/bash

ct_list_file=/tmp/pct_alive

pct list | grep running | cut -d' ' -f1 > $ct_list_file

for ct in $(cat $ct_list_file); do
	echo "Restarting $ct"
	pct stop $ct && pct start $ct
done
