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
        self._timeline.append((t1 - t2).seconds)
        for t in range(1, len(self._timestamps)):
            t1 = self._timestamps[t]
            t2 = self._timestamps[t - 1]
            self._timeline.append((t1 - t2).seconds)
        #print("Timeline: {}".format(self._timeline))

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
                    self._timestamps.append(datetime.strptime(time, "%H:%M:%S"))
                    self._sent.append(float(sent))
                    self._received.append(float(received))
            except Exception as e:
                print("ERROR: {} for parsing line: {}".format(e, line))
        #self.convert_timestamps()
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
                    self._timestamps.append(datetime.strptime(time, "%H:%M:%S"))
                    self._cpu.append(float(cpu))
                    self._mem.append(float(mem))
                    print(self._cpu)
            except Exception as e:
                print("ERROR: {} for parsing line: {}".format(e, line))
        #self.convert_timestamps()
        print("Top lines: {}".format(len(self._lines)))

    @property
    def cpu(self):
        return self._cpu

    @property
    def mem(self):
        return self._mem

if __name__ == "__main__":
    nethogs = NethogsParser("lcrail-nethogs-test.txt", "firefox")
    nethogs.parse()
    top = TopParser("lcrail-top-test.txt", "firefox")
    top.parse()
    plt.title("CPU usage")
    plt.plot(top.cpu)
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.show()
    plt.title("RAM usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.plot(top.mem)
    plt.show()
    plt.title("Network usage")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (MB)")
    plt.plot(nethogs.sent, label="Sent")
    plt.plot(nethogs.received, label="Received")
    plt.legend()
    plt.show()
