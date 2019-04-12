#!/bin/python
import argparse
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import glob
import sys
import statistics
from datetime import datetime
BAR_WIDTH = 0.8
COLOR_JOLLA_1 = "#c9211e"
COLOR_XPERIA_X = "#3465a4"
COLOR_ORIGINAL = "#c9211e"
COLOR_RT_POLL = "#3465a4"
COLOR_RT_SSE = "#127622"
X_POS = [1, 3, 5]

class Plotter():
    def __init__(self, data, bar_width=BAR_WIDTH):
        self._data = data
        self._bar_width = bar_width

        # Set figure size
        plt.rcParams["figure.figsize"] = [8, 5]

    def legend_bar(self):
        custom_lines = [Line2D([0], [0], color=COLOR_XPERIA_X, lw=4),
                        Line2D([0], [0], color=COLOR_JOLLA_1, lw=4)]
        plt.legend(custom_lines, ["Xperia X", "Jolla 1"])

    def legend_plot(self):
        custom_lines = [Line2D([0], [0], color=COLOR_ORIGINAL, lw=4),
                        Line2D([0], [0], color=COLOR_RT_POLL, lw=4),
                        Line2D([0], [0], color=COLOR_RT_SSE, lw=4)]
        plt.legend(custom_lines, ["Original", "RT polling", "RT SSE"])

    def axis_labels_bar(self, y_max, y_label, unit):
        # X labels
        x = np.array(X_POS)
        my_xticks = ["Original", "RT polling", "RT SSE"]
        plt.xticks(x, my_xticks)

        # Y labels
        plt.ylabel("{} ({})".format(y_label, unit))
        plt.ylim(0, 1.5 * y_max)

    def axis_labels_plot(self, y_max, y_label, unit):
        # X labels
        plt.xlabel("Time (ms)")

        # Y labels
        plt.ylabel("{} ({})".format(y_label, unit))
        plt.ylim(0, 1.5 * y_max)

    def color_device(self, device):
        if device == "jolla-1":
            return COLOR_JOLLA_1
        elif device == "xperia-x":
            return COLOR_XPERIA_X
        else:
            raise NotImplementedError("Unknown device, no color available!")

    def color_name(self, name):
        if name == "original":
            return COLOR_ORIGINAL
        elif name == "rt-poll":
            return COLOR_RT_POLL
        elif name == "rt-sse":
            return COLOR_RT_SSE
        else:
            raise NotImplementedError("Unknown name, cannot determine color")

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

    def bar_values(self, bar_graph, unit, rounding):
        # Draw values on top of each bar
        for bar in bar_graph:
            y = bar.get_height()
            y_value = round(y, rounding)
            if rounding == 0:
                y_value = int(y_value)
            plt.text(bar.get_x() + self._bar_width/2,
                     1.05 * y,
                     "{} {}".format(y_value, unit),
                     va="bottom",
                     ha="center",
                     fontweight="bold",
                     fontsize=10)

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
            plt.title("RAM usage (liveboard)")
        else:
            raise NotImplementedError("Unknown benchmark name ({}) and mode ({})".format(name, mode))

        # Set figure size
        plt.rcParams["figure.figsize"] = [8, 5]

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
                                        color=self.color_device(device))
                            self.bar_values(b, unit, 1)

        # Legend and axis labels
        self.legend_bar()
        self.axis_labels_bar(y_max, "Usage", unit)
        plt.show()

    def plot_nethogs_mean(self, name, mode="sent"):
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

        # Set figure size
        plt.rcParams["figure.figsize"] = [8, 5]

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
                                        color=self.color_device(device))
                            self.bar_values(b, unit, 1)

        # Legend and axis labels
        self.legend_bar()
        self.axis_labels_bar(y_max, "Usage", unit)
        plt.show()

    def plot_nethogs_all(self, name, mode="sent", device="xperia-x"):
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

        # Set figure size
        plt.rcParams["figure.figsize"] = [8, 5]

        # X-axis data
        y_max = 0
        unit = "MB"
        for benchmark in self._data:
            for part in self._data[benchmark]:
                if name in part:
                    for device_name in self._data[benchmark][part]:
                        if "nethogs" in self._data[benchmark][part][device_name] and device == device_name:
                            # Find the maximum value (nethogs = accumulated)
                            accumulated = self._data[benchmark][part][device_name]["nethogs"][mode][-1]
                            data = self._data[benchmark][part][device_name]["nethogs"][mode]
                            timeline = self._data[benchmark][part][device_name]["nethogs"]["timeline"]

                            # Keep the maximum value
                            if accumulated > y_max:
                                y_max = accumulated

                            # Plot
                            plt.plot(timeline, data, color=self.color_name(benchmark))

        # Legend and axis labels
        self.legend_plot()
        self.axis_labels_plot(y_max, "Usage", unit)
        plt.show()

    def plot_user_informed_time(self, name):
        # Generate beautiful title
        if name == "planner":
            plt.title("Refresh time (CSA)")
        elif name == "liveboard":
            plt.title("Refresh time (liveboard)")
        else:
            raise NotImplementedError("Unknown benchmark name ({}) and mode ({})".format(name, mode))

        # Set figure size
        plt.rcParams["figure.figsize"] = [8, 5]

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
                                        color=self.color_device(device))
                            self.bar_values(b, unit, 0)

        # Legend and axis labels
        self.legend_bar()
        self.axis_labels_bar(y_max, "Time", unit)
        plt.show()

