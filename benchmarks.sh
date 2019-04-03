#!/bin/bash
top -p $1 -b > lcrail-top-$2.txt
nethogs -v 3 -t > lcrail-nethogs-$2.txt
