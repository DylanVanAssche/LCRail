#!/bin/python
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
                    day, month, date, time, year, timezone = timestamp.split()
                    if "liveboard" in name:
                        self._liveboard_timestamps.append(datetime.strptime(time, "%H:%M:%S").timestamp())
                    elif "planner" in name:
                        self._planner_timestamps.append(datetime.strptime(time, "%H:%M:%S").timestamp())
                    else:
                        raise NotImplementedError("Unknown benchmark name")
            except Exception as e:
                print("ERROR: {} for parsing line: {}".format(e, line))
        self.convert_liveboard()
        self.convert_planner()

    def convert_liveboard(self):
        # Liveboard starts with a timestamp and ends with a timestamp, both are always in pairs
        for l in range(0, len(self._liveboard_timestamps), 2):
            liveboard_requested = self._liveboard_timestamps[l]
            liveboard_processed = self._liveboard_timestamps[l + 1]
            self._liveboard.append(liveboard_processed - liveboard_requested)
        print("Liveboard lines: {}".format(len(self._liveboard)))

    def convert_planner(self):
        # Planner starts with a timestamp and ends with a timestamp, both are always in pairs
        for l in range(0, len(self._planner_timestamps), 2):
            planner_requested = self._planner_timestamps[l]
            planner_processed = self._planner_timestamps[l + 1]
            self._planner.append(planner_processed - planner_requested)
        print("Planner lines: {}".format(len(self._planner)))

    @property
    def liveboard(self):
        return self._liveboard

    @property
    def planner(self):
        return self._planner


if __name__ == "__main__":
    # Parse Nethogs
    nethogs = NethogsParser("lcrail-nethogs-original3.txt", "lcrail")
    nethogs.parse()

    # Parse Top
    top = TopParser("lcrail-top-original3.txt", "lcrail")
    top.parse()

    # Parse User Informed Time
    user_informed_time = UserInformedTimeParser("lcrail-userinformedtime-original3.txt")
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
    plt.plot(top.timeline, top.cpu)
    plt.plot(top.timeline, top.mem)
    plt.show()

    # Network usage
    plt.title("Network usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (MB)")
    plt.plot(nethogs.timeline, nethogs.sent, label="Sent")
    plt.plot(nethogs.timeline, nethogs.received, label="Received")
    plt.legend()
    plt.show()

    # Liveboard refresh time
    plt.title("Liveboard refresh time")
    plt.ylabel("Time (s)")
    plt.xlabel("Measurement")
    plt.boxplot(user_informed_time.liveboard)
    plt.show()

    # Planner refresh time
    plt.title("Planner refresh time")
    plt.ylabel("Time (s)")
    plt.xlabel("Measurement")
    plt.boxplot(user_informed_time.planner)
    plt.show()
