#!/bin/python
import argparse
import matplotlib.pyplot as plt
import glob
import sys
import statistics
from datetime import datetime


class BaseParser:
    def __init__(self, input_file, process=None):
        self._input_file = input_file
        self._lines = []
        self._timestamps = []
        self._timeline = [] # Start at 0s
        self._process = process
        self.read_file()

    def read_file(self):
        with open(self._input_file, "r") as f:
           self._lines = f.readlines()

    def parse(self):
        raise NotImplementedError("Parsing method is absent")

    def convert_timestamps(self):
        # Convert timestamps to timeline
        if not self._timestamps:
            return

        begin_timestamp = self._timestamps[0]
        for t in self._timestamps:
            self._timeline.append(t - begin_timestamp)

    @property
    def timeline(self):
        return self._timeline

class NethogsParser(BaseParser):
    def __init__(self, input_file, process):
        super().__init__(input_file, process)
        self._sent = []
        self._received = []

    def parse(self):
        for line in self._lines:
            try:
                if self._process in line:
                    day, month, date, time, timezone, year, process, sent, received = line.split()
                    self._timestamps.append(datetime.strptime(time, "%H:%M:%S").timestamp())
                    self._sent.append(float(sent))
                    self._received.append(float(received))
            except Exception as e:
                print("\nERROR: {} for parsing line: {} in file {}".format(e, line, self._input_file), file=sys.stderr)
        self.convert_timestamps()

    @property
    def sent(self):
        return self._sent

    @property
    def received(self):
        return self._received

class TopParser(BaseParser):
    def __init__(self, input_file, process):
        super().__init__(input_file, process)
        self._cpu = []
        self._mem = []

    def parse(self):
        for line in self._lines:
            try:
                if self._process in line:
                    day, month, date, time, timezone, year, pid, user, priority, nice, virtual_mem, res, shr, state, cpu, mem, cputime, command = line.split()
                    self._timestamps.append(datetime.strptime(time, "%H:%M:%S").timestamp())
                    self._cpu.append(float(cpu))
                    self._mem.append(float(mem))
            except Exception as e:
                print("\nERROR: {} for parsing line: {} in file {}".format(e, line, self._input_file), file=sys.stderr)
        self.convert_timestamps()

    @property
    def cpu(self):
        return self._cpu

    @property
    def mem(self):
        return self._mem

class UserInformedTimeParser(BaseParser):
    def __init__(self, input_file):
        super().__init__(input_file)
        self._liveboard_timestamps = []
        self._planner_timestamps = []
        self._liveboard = []
        self._planner = []

    def parse(self):
        for line in self._lines:
            try:
                if "$" in line:
                    _, name, timestamp = line.split(",")
                    if "liveboard" in name:
                        self._liveboard.append(abs(int(timestamp)))
                    elif "router" in name:
                        self._planner.append(abs(int(timestamp)))
                    else:
                        raise NotImplementedError("Unknown benchmark name")
            except ValueError as e:
                pass # Ignore unused log 
            except Exception as e:
                print("\nERROR: {} for parsing line: {} in file {}".format(e, line, self._input_file), file=sys.stderr)

    @property
    def liveboard(self):
        return self._liveboard

    @property
    def planner(self):
        return self._planner


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="LCRail benchmark.")
    parser.add_argument("process",
                        type=str,
                        help="The name of the benchmarked process , for example: <process>-top-<name>.txt")
    args = parser.parse_args()
    process = args.process
    print("Benchmarking process: {}".format(process))

    data = {}
    files = glob.glob("results/**/**/**/*.txt", recursive=True)
    for i, path in enumerate(files):
        percentage = ((i + 1) / len(files)) * 100
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %d%%" % ('=' * int(percentage), percentage))
        sys.stdout.flush()
        _, benchmark, part, device, filename = path.split("/")

        # Create data tree
        if not benchmark in data:
            data[benchmark] = {}

        if not part in data[benchmark]:
            data[benchmark][part] = {}

        if not device in data[benchmark][part]:
            data[benchmark][part][device] = {}

        # Nethogs file
        if "nethogs" in path:
            nethogs = NethogsParser(path, process)
            nethogs.parse()
            data[benchmark][part][device]["nethogs"] = {
                                                            "sent": nethogs.sent,
                                                            "received": nethogs.received,
                                                            "timeline": nethogs.timeline
                                                       }

        # Top file
        elif "top" in path:
            top = TopParser(path, process)
            top.parse()
            data[benchmark][part][device]["top"] = {
                                                        "cpu": top.cpu,
                                                        "mem": top.mem,
                                                        "timeline": top.timeline
                                                   }
        else:
            user_informed_time = UserInformedTimeParser(path)
            user_informed_time.parse()
            data[benchmark][part][device]["user_informed_time"] = {}

            # Liveboard data
            if user_informed_time.liveboard:
                data[benchmark][part][device]["user_informed_time"]["liveboard"] = user_informed_time.liveboard
                data[benchmark][part][device]["user_informed_time"]["timeline"] = len(user_informed_time.liveboard)

            # Planner data
            if user_informed_time.planner:
                data[benchmark][part][device]["user_informed_time"]["planner"] = user_informed_time.planner
                data[benchmark][part][device]["user_informed_time"]["timeline"] = len(user_informed_time.planner)

    ROUNDING = 1
    TEXT_DISTANCE = 0.5


    # CPU usage
    plt.title("CPU usage liveboard")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.ylim(0, 20)
    cpu_count = 0
    position = {
        "original": {
            "base": 2,
            "width": 0.5,
            "xperia-x": -0.25,
            "jolla-1": 0.25
        },
        "rt-poll": {
            "base": 4,
            "width": 0.5,
            "xperia-x": -0.25,
            "jolla-1": 0.25
        },
        "rt-sse": {
            "base": 6,
            "width": 0.5,
            "xperia-x": -0.25,
            "jolla-1": 0.25
        }
    }
    for benchmark in data:
        for part in data[benchmark]:
            if "liveboard" in part:
                for device in data[benchmark][part]:
                    if "top" in data[benchmark][part][device]:
                        mean = statistics.mean(data[benchmark][part][device]["top"]["cpu"])
                        color = "r"
                        if "jolla" in device:
                            color = "b"
                        b = plt.bar(position[benchmark]["base"] + position[benchmark][device], mean,
                                    width=0.5,
                                    label=(benchmark + "@" + device),
                                   align="center", color=color)
                        # access the bar attributes to place the text in the appropriate location
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING),
                                     va="center", fontweight="bold")
                        cpu_count += 1
    plt.legend()
    plt.show()

    # RAM usage
    plt.title("RAM usage liveboard")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.ylim(0, 20)
    mem_count = 0
    for benchmark in data:
        for part in data[benchmark]:
            if "liveboard" in part:
                for device in data[benchmark][part]:
                    if "top" in data[benchmark][part][device]:
                        mean = statistics.mean(data[benchmark][part][device]["top"]["mem"])
                        b = plt.bar(mem_count, mean, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING),
                                     va="center", fontweight="bold")
                        mem_count += 1
    plt.legend()
    plt.show()

    # CPU usage
    plt.title("CPU usage planner")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.ylim(0, 50)
    cpu_count = 0
    for benchmark in data:
        for part in data[benchmark]:
            if "planner" in part:
                for device in data[benchmark][part]:
                    if "top" in data[benchmark][part][device]:
                        mean = statistics.mean(data[benchmark][part][device]["top"]["cpu"])
                        b = plt.bar(cpu_count, mean, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        cpu_count += 1
    plt.legend()
    plt.show()

    # RAM usage
    plt.title("RAM usage planner")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.ylim(0, 20)
    mem_count = 0
    for benchmark in data:
        for part in data[benchmark]:
            if "planner" in part:
                for device in data[benchmark][part]:
                    if "top" in data[benchmark][part][device]:
                        mean = statistics.mean(data[benchmark][part][device]["top"]["mem"])
                        b = plt.bar(mem_count, mean, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        mem_count += 1
    plt.legend()
    plt.show()

    # Network usage
    plt.title("Network usage Planner")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    #plt.ylim(0, 20)
    network_count = 0
    for benchmark in data:
        for part in data[benchmark]:
            if "planner" in part:
                for device in data[benchmark][part]:
                    if "nethogs" in data[benchmark][part][device]:
                        total_sent = data[benchmark][part][device]["nethogs"]["sent"][-1]
                        total_received = data[benchmark][part][device]["nethogs"]["received"][-1]
                        b = plt.bar(network_count, total_sent, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        b = plt.bar(network_count + 1, total_received, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        network_count += 2
    plt.legend()
    plt.show()

    # Network usage
    plt.title("Network usage Liveboard")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    #plt.ylim(0, 20)
    network_count = 0
    for benchmark in data:
        for part in data[benchmark]:
            if "liveboard" in part:
                for device in data[benchmark][part]:
                    if "nethogs" in data[benchmark][part][device]:
                        total_sent = data[benchmark][part][device]["nethogs"]["sent"][-1]
                        total_received = data[benchmark][part][device]["nethogs"]["received"][-1]
                        b = plt.bar(network_count, total_sent, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        b = plt.bar(network_count + 1, total_received, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        network_count += 2
    plt.legend()
    plt.show()

    # Refresh time 
    plt.title("Refresh time Liveboard")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    #plt.ylim(0, 20)
    refresh_count = 0
    for benchmark in data:
        for part in data[benchmark]:
            if "liveboard" in part:
                for device in data[benchmark][part]:
                    if "user_informed_time" in data[benchmark][part][device]:
                        refresh_time = statistics.mean(data[benchmark][part][device]["user_informed_time"]["liveboard"])
                        b = plt.bar(refresh_count, refresh_time, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        refresh_count += 1
    plt.legend()
    plt.show()

    # Refresh time 
    plt.title("Refresh time Planner")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    #plt.ylim(0, 20)
    refresh_count = 0
    for benchmark in data:
        for part in data[benchmark]:
            if "planner" in part:
                for device in data[benchmark][part]:
                    if "user_informed_time" in data[benchmark][part][device]:
                        refresh_time = statistics.mean(data[benchmark][part][device]["user_informed_time"]["planner"])
                        b = plt.bar(refresh_count, refresh_time, label=(benchmark + "@" + device))
                        for bar in b:
                            yval = bar.get_height()
                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
                        refresh_count += 1
    plt.legend()
    plt.show()
    exit()

    # Network usage
    plt.title("Network usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (MB)")
    plt.ylim(0, 10)
    plt.plot(nethogs.timeline, nethogs.sent, label="Sent")
    plt.plot(nethogs.timeline, nethogs.received, label="Received")
    plt.legend()
    plt.show()

    # Liveboard refresh time
    plt.title("Liveboard refresh time")
    plt.ylabel("Time (ms)")
    plt.ylim(0, 15000)
    plt.xlabel("Measurement")
    #plt.boxplot(user_informed_time.liveboard)
    plt.bar(range(0, len(user_informed_time.liveboard)), user_informed_time.liveboard)
    plt.show()

    # Planner refresh time
    plt.title("Planner refresh time")
    plt.ylabel("Time (ms)")
    plt.ylim(0, 30000)
    plt.xlabel("Measurement")
    plt.bar(range(0, len(user_informed_time.planner)), user_informed_time.planner)
    #plt.boxplot(user_informed_time.planner)
    plt.show()
