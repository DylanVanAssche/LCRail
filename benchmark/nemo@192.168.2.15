#!/bin/bash
adddate() {
    while IFS= read -r line; do
        echo "$(date) $line"
    done
}

top -p $1 -b | adddate >> lcrail-top-$2.txt &
P1=$!
nethogs -d enp0s29u1u1  -v 3 -t | adddate >> lcrail-nethogs-$2.txt &
P2=$!
wait $P1 $P2
