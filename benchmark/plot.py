#!/bin/python
import argparse
import matplotlib.pyplot as plt
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
                print("ERROR: {} for parsing line: {}".format(e, line))
        self.convert_timestamps()
        print("Nethogs lines: {}".format(len(self._sent)))

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
                print("ERROR: {} for parsing line: {}".format(e, line))
        self.convert_timestamps()
        print("Top lines: {}".format(len(self._cpu)))

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
                    print(timestamp)
                    if "liveboard" in name:
                        self._liveboard.append(abs(int(timestamp)))
                    elif "router" in name:
                        self._planner.append(abs(int(timestamp)))
                    else:
                        raise NotImplementedError("Unknown benchmark name")
            except Exception as e:
                print("ERROR: {} for parsing line: {}".format(e, line))

    @property
    def liveboard(self):
        return self._liveboard

    @property
    def planner(self):
        return self._planner


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="LCRail benchmark.")
    parser.add_argument("name",
                        type=str,
                        help="The name of the benchmark file, for example: <process>-top-<name>.txt")
    parser.add_argument("process",
                        type=str,
                        help="The name of the benchmarked process , for example: <process>-top-<name>.txt")
    args = parser.parse_args()
    process = args.process
    name = args.name
    print("Process: {}".format(process))
    print("Name: {}".format(name))


    # Parse Nethogs
    nethogs = NethogsParser("{}-nethogs-{}.txt".format(process, name), process)
    nethogs.parse()

    # Parse Top
    top = TopParser("{}-top-{}.txt".format(process, name), process)
    top.parse()

    # Parse User Informed Time
    user_informed_time = UserInformedTimeParser("{}-{}.txt".format(process, name))
    user_informed_time.parse()

    # CPU usage
    plt.title("CPU usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.ylim(0, 100)
    plt.plot(top.timeline, top.cpu)
    plt.show()

    # RAM usage
    plt.title("RAM usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.ylim(0, 25)
    plt.plot(top.timeline, top.mem)
    plt.show()

    # CPU and RAM usage
    plt.title("CPU and RAM usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.ylim(0, 100)
    plt.plot(top.timeline, top.cpu, label="CPU")
    plt.plot(top.timeline, top.mem, label="RAM")
    plt.legend()
    plt.show()

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
