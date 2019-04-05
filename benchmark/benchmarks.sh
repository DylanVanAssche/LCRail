#!/bin/bash
# Dylan Van Assche - LCRail benchmark
# Usage: # ./benchmark.sh <benchmark name>

# Add timestamp in front of the current line
adddate() {
    while IFS= read -r line; do
        echo "$(date) $line"
    done
}

# Plot the Top CPU and RAM statistics of all processes
top -b | adddate >> lcrail-top-$1.txt &
P1=$!

# Plot the Nethogs network traffic statistics of all processes
nethogs -v 3 -t | adddate >> lcrail-nethogs-$1.txt &
P2=$!

# Wait until both background processes are killed when we kill our script
wait $P1 $P2
