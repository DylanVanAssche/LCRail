#!/bin/python
import matplotlib.pyplot as plt
from datetime import datetime


class BaseParser:
    def __init__(self, input_file, process):
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
        print("Nethogs lines: {}".format(len(self._lines)))

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
                    print(self._cpu)
            except Exception as e:
                print("ERROR: {} for parsing line: {}".format(e, line))
        self.convert_timestamps()
        print("Top lines: {}".format(len(self._lines)))

    @property
    def cpu(self):
        return self._cpu

    @property
    def mem(self):
        return self._mem

if __name__ == "__main__":
    nethogs = NethogsParser("lcrail-nethogs-original.txt", "lcrail")
    nethogs.parse()
    top = TopParser("lcrail-top-original.txt", "lcrail")
    top.parse()
    plt.title("CPU usage")
    plt.plot(top.timeline, top.cpu)
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.show()
    plt.title("RAM usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.plot(top.timeline, top.mem)
    plt.show()
    plt.title("Network usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (MB)")
    plt.plot(nethogs.timeline, nethogs.sent, label="Sent")
    plt.plot(nethogs.timeline, nethogs.received, label="Received")
    plt.legend()
    plt.show()
