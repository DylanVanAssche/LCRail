#!/bin/bash
adddate() {
    while IFS= read -r line; do
        echo "$(date) $line"
    done
}

top -b | adddate >> lcrail-top-$2.txt &
P1=$!
nethogs -v 3 -t | adddate >> lcrail-nethogs-$2.txt &
P2=$!
wait $P1 $P2