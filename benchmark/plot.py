#!/bin/python
import argparse
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import glob
import sys
import statistics
from datetime import datetime
ROUNDING = 1
BAR_WIDTH = 0.8
COLOR_JOLLA_1 = "#c9211e"
COLOR_XPERIA_X = "#3465a4"
X_POS = [1, 3, 5]

class Plotter():
    def __init__(self, data, rounding=ROUNDING, bar_width=BAR_WIDTH):
        self._data = data
        self._rounding = rounding
        self._bar_width = bar_width

    def legend(self):
        custom_lines = [Line2D([0], [0], color=COLOR_XPERIA_X, lw=4),
                        Line2D([0], [0], color=COLOR_JOLLA_1, lw=4)]
        plt.legend(custom_lines, ["Xperia X", "Jolla 1"])

    def axis_labels(self, y_max, y_label, unit):
        # X labels
        x = np.array(X_POS)
        my_xticks = ["Original", "RT polling", "RT SSE"]
        plt.xticks(x, my_xticks)

        # Y labels
        plt.ylabel("{} ({})".format(y_label, unit))
        plt.ylim(0, 1.5 * y_max)

    def color(self, device):
        if device == "jolla-1":
            return COLOR_JOLLA_1
        elif device == "xperia-x":
            return COLOR_XPERIA_X
        else:
            raise NotImplementedError("Unknown device, no color available!")

    def position(self, name):
        if name == "original":
            return X_POS[0]
        elif name == "rt-poll":
            return X_POS[1]
        elif name == "rt-sse":
            return X_POS[2]
        else:
            raise NotImplementedError("Unknown name, cannot determine bar position")

    def position_move(self, device):
        if device == "jolla-1":
            return -self._bar_width/2.0
        elif device == "xperia-x":
            return self._bar_width/2.0
        else:
            raise NotImplementedError("Unknown device, no color available!")

    def bar_values(self, bar_graph, unit):
        # Draw values on top of each bar
        for bar in bar_graph:
            y = bar.get_height()
            plt.text(bar.get_x() + self._bar_width/2,
                     1.05 * y,
                     "{} {}".format(round(y, self._rounding), unit),
                     va="bottom",
                     ha="center",
                     fontweight="bold")

    def plot_top(self, name, mode="cpu"):
        # Check if implemented
        assert(mode == "cpu" or mode == "mem")
        assert(name == "planner" or name == "liveboard")

        # Generate beautiful title
        if mode == "cpu" and name == "planner":
            plt.title("CPU usage (CSA)")
        elif mode == "cpu" and name == "liveboard":
            plt.title("CPU usage (liveboard)")
        elif mode == "mem" and name == "planner":
            plt.title("RAM usage (CSA)")
        elif mode == "mem" and name == "liveboard":
            plt.title("RAM usage (liveboard")
        else:
            raise NotImplementedError("Unknown benchmark name ({}) and mode ({})".format(name, mode))

        # X-axis data
        y_max = 0
        unit = "%"
        for benchmark in self._data:
            for part in self._data[benchmark]:
                if name in part:
                    for device in self._data[benchmark][part]:
                        if "top" in self._data[benchmark][part][device]:
                            # Find the mean value
                            mean = statistics.mean(self._data[benchmark][part][device]["top"][mode])

                            # Keep the maximum value
                            if mean > y_max:
                                y_max = mean

                            # Draw bar
                            b = plt.bar(self.position(benchmark) + self.position_move(device),
                                        mean,
                                        width=self._bar_width,
                                        align="center",
                                        color=self.color(device))
                            self.bar_values(b, unit)

        # Legend and axis labels
        self.legend()
        self.axis_labels(y_max, "Usage", unit)
        plt.show()


    def plot_nethogs(self, name, mode="sent"):
        # Generate beautiful title
        if mode == "sent" and name == "planner":
            plt.title("Network sent (CSA)")
        elif mode == "sent" and name == "liveboard":
            plt.title("Network sent (liveboard)")
        elif mode == "received" and name == "planner":
            plt.title("Network received (CSA)")
        elif mode == "received" and name == "liveboard":
            plt.title("Network received (liveboard)")
        else:
            raise NotImplementedError("Unknown benchmark name ({}) and mode ({})".format(name, mode))

        # X-axis data
        y_max = 0
        unit = "MB"
        for benchmark in self._data:
            for part in self._data[benchmark]:
                if name in part:
                    for device in self._data[benchmark][part]:
                        if "nethogs" in self._data[benchmark][part][device]:
                            # Find the maximum value (nethogs = accumulated)
                            accumulated = self._data[benchmark][part][device]["nethogs"][mode][-1]

                            # Keep the maximum value
                            if accumulated > y_max:
                                y_max = accumulated

                            # Draw bar
                            b = plt.bar(self.position(benchmark) + self.position_move(device),
                                        accumulated,
                                        width=self._bar_width,
                                        align="center",
                                        color=self.color(device))
                            self.bar_values(b, unit)

        # Legend and axis labels
        self.legend()
        self.axis_labels(y_max, "Usage", unit)
        plt.show()


    def plot_user_informed_time(self, name):
        # Generate beautiful title
        if name == "planner":
            plt.title("Refresh time (CSA)")
        elif name == "liveboard":
            plt.title("Refresh time (liveboard)")
        else:
            raise NotImplementedError("Unknown benchmark name ({}) and mode ({})".format(name, mode))

        # X-axis data
        y_max = 0
        unit = "ms"
        for benchmark in self._data:
            for part in self._data[benchmark]:
                if name in part:
                    for device in self._data[benchmark][part]:
                        if "user_informed_time" in self._data[benchmark][part][device]:
                            # Find the mean value
                            mean = statistics.mean(self._data[benchmark][part][device]["user_informed_time"][name])

                            # Keep the maximum value
                            if mean > y_max:
                                y_max = mean

                            # Draw bar
                            b = plt.bar(self.position(benchmark) + self.position_move(device),
                                        mean,
                                        width=self._bar_width,
                                        align="center",
                                        color=self.color(device))
                            self.bar_values(b, unit)

        # Legend and axis labels
        self.legend()
        self.axis_labels(y_max, "Time", unit)
        plt.show()




#    # RAM usage
#    plt.title("RAM usage liveboard")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (%)")
#    plt.ylim(0, 20)
#    mem_count = 0
#    for benchmark in self.data:
#        for part in data[benchmark]:
#            if "liveboard" in part:
#                for device in data[benchmark][part]:
#                    if "top" in data[benchmark][part][device]:
#                        mean = statistics.mean(data[benchmark][part][device]["top"]["mem"])
#                        b = plt.bar(mem_count, mean, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING),
#                                     va="center", fontweight="bold")
#                        mem_count += 1
#    plt.legend()
#    plt.show()
#
#    # CPU usage
#    plt.title("CPU usage planner")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (%)")
#    plt.ylim(0, 50)
#    cpu_count = 0
#    for benchmark in data:
#        for part in data[benchmark]:
#            if "planner" in part:
#                for device in data[benchmark][part]:
#                    if "top" in data[benchmark][part][device]:
#                        mean = statistics.mean(data[benchmark][part][device]["top"]["cpu"])
#                        b = plt.bar(cpu_count, mean, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        cpu_count += 1
#    plt.legend()
#    plt.show()
#
#    # RAM usage
#    plt.title("RAM usage planner")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (%)")
#    plt.ylim(0, 20)
#    mem_count = 0
#    for benchmark in data:
#        for part in data[benchmark]:
#            if "planner" in part:
#                for device in data[benchmark][part]:
#                    if "top" in data[benchmark][part][device]:
#                        mean = statistics.mean(data[benchmark][part][device]["top"]["mem"])
#                        b = plt.bar(mem_count, mean, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        mem_count += 1
#    plt.legend()
#    plt.show()
#
#    # Network usage
#    plt.title("Network usage Planner")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (%)")
#    #plt.ylim(0, 20)
#    network_count = 0
#    for benchmark in data:
#        for part in data[benchmark]:
#            if "planner" in part:
#                for device in data[benchmark][part]:
#                    if "nethogs" in data[benchmark][part][device]:
#                        total_sent = data[benchmark][part][device]["nethogs"]["sent"][-1]
#                        total_received = data[benchmark][part][device]["nethogs"]["received"][-1]
#                        b = plt.bar(network_count, total_sent, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        b = plt.bar(network_count + 1, total_received, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        network_count += 2
#    plt.legend()
#    plt.show()
#
#    # Network usage
#    plt.title("Network usage Liveboard")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (%)")
#    #plt.ylim(0, 20)
#    network_count = 0
#    for benchmark in data:
#        for part in data[benchmark]:
#            if "liveboard" in part:
#                for device in data[benchmark][part]:
#                    if "nethogs" in data[benchmark][part][device]:
#                        total_sent = data[benchmark][part][device]["nethogs"]["sent"][-1]
#                        total_received = data[benchmark][part][device]["nethogs"]["received"][-1]
#                        b = plt.bar(network_count, total_sent, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        b = plt.bar(network_count + 1, total_received, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        network_count += 2
#    plt.legend()
#    plt.show()
#
#    # Refresh time 
#    plt.title("Refresh time Liveboard")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (%)")
#    #plt.ylim(0, 20)
#    refresh_count = 0
#    for benchmark in data:
#        for part in data[benchmark]:
#            if "liveboard" in part:
#                for device in data[benchmark][part]:
#                    if "user_informed_time" in data[benchmark][part][device]:
#                        refresh_time = statistics.mean(data[benchmark][part][device]["user_informed_time"]["liveboard"])
#                        b = plt.bar(refresh_count, refresh_time, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        refresh_count += 1
#    plt.legend()
#    plt.show()
#
#    # Refresh time 
#    plt.title("Refresh time Planner")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (%)")
#    #plt.ylim(0, 20)
#    refresh_count = 0
#    for benchmark in data:
#        for part in data[benchmark]:
#            if "planner" in part:
#                for device in data[benchmark][part]:
#                    if "user_informed_time" in data[benchmark][part][device]:
#                        refresh_time = statistics.mean(data[benchmark][part][device]["user_informed_time"]["planner"])
#                        b = plt.bar(refresh_count, refresh_time, label=(benchmark + "@" + device))
#                        for bar in b:
#                            yval = bar.get_height()
#                            plt.text(bar.get_x(), yval + TEXT_DISTANCE, round(yval, ROUNDING))
#                        refresh_count += 1
#    plt.legend()
#    plt.show()
#    exit()
#
#    # Network usage
#    plt.title("Network usage")
#    plt.xlabel("Time (s)")
#    plt.ylabel("Usage (MB)")
#    plt.ylim(0, 10)
#    plt.plot(nethogs.timeline, nethogs.sent, label="Sent")
#    plt.plot(nethogs.timeline, nethogs.received, label="Received")
#    plt.legend()
#    plt.show()
#
#    # Liveboard refresh time
#    plt.title("Liveboard refresh time")
#    plt.ylabel("Time (ms)")
#    plt.ylim(0, 15000)
#    plt.xlabel("Measurement")
#    #plt.boxplot(user_informed_time.liveboard)
#    plt.bar(range(0, len(user_informed_time.liveboard)), user_informed_time.liveboard)
#    plt.show()
#
#    # Planner refresh time
#    plt.title("Planner refresh time")
#    plt.ylabel("Time (ms)")
#    plt.ylim(0, 30000)
#    plt.xlabel("Measurement")
#    plt.bar(range(0, len(user_informed_time.planner)), user_informed_time.planner)
#    #plt.boxplot(user_informed_time.planner)
#    plt.show()
