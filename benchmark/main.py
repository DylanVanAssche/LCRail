#!/bin/python
import argparse
import glob
import sys
from parser import TopParser, NethogsParser, UserInformedTimeParser
from plot import Plotter

class Main():
    def __init__(self, path, process):
        self._path = path
        self._process = process
        self._data = {}
        print("Benchmarking process: {}".format(process))

    def run(self):
        # Recursive discover all files
        files = glob.glob(self._path, recursive=True)

        # Build the self._data tree by parsing each file correctly
        number_of_files = len(files)
        for i, path in enumerate(files):
            self.print_progress(i, number_of_files)

            # Retrieve current file meta self._data based on path
            _, benchmark, part, device, filename = path.split("/")

            # Create self._data tree if needed
            self.create_data_tree(benchmark, part, device)

            # Nethogs file
            if "nethogs" in path:
                nethogs = NethogsParser(path, self._process)
                nethogs.parse()
                self._data[benchmark][part][device]["nethogs"] = {
                                                                "sent": nethogs.sent,
                                                                "received": nethogs.received,
                                                                "timeline": nethogs.timeline
                                                           }

            # Top file
            elif "top" in path:
                top = TopParser(path, self._process)
                top.parse()
                self._data[benchmark][part][device]["top"] = {
                                                            "cpu": top.cpu,
                                                            "mem": top.mem,
                                                            "timeline": top.timeline
                                                       }
            # User Informed Time file
            else:
                user_informed_time = UserInformedTimeParser(path)
                user_informed_time.parse()
                self._data[benchmark][part][device]["user_informed_time"] = {}

                # Liveboard
                if user_informed_time.liveboard:
                    self._data[benchmark][part][device]["user_informed_time"]["liveboard"] = user_informed_time.liveboard
                    self._data[benchmark][part][device]["user_informed_time"]["timeline"] = len(user_informed_time.liveboard)

                # Planner
                if user_informed_time.planner:
                    self._data[benchmark][part][device]["user_informed_time"]["planner"] = user_informed_time.planner
                    self._data[benchmark][part][device]["user_informed_time"]["timeline"] = len(user_informed_time.planner)

        # Parsing complete
        print("\nFinished parsing, processing plots...")

        # Plot all the data using the Plotter class
        p = Plotter(self._data)

        # CPU and RAM usage
        p.plot_top("liveboard", "cpu")
        p.plot_top("liveboard", "mem")
        p.plot_top("planner", "cpu")
        p.plot_top("planner", "mem")

        # Network usage
        p.plot_nethogs("liveboard", "sent")
        p.plot_nethogs("liveboard", "received")
        p.plot_nethogs("planner", "sent")
        p.plot_nethogs("planner", "received")

        # Refresh time
        p.plot_user_informed_time("liveboard")
        p.plot_user_informed_time("planner")

    def print_progress(self, file_index, number_of_files):
        # Calculate percentage and generate progress bar
        percentage = ((file_index + 1) / number_of_files) * 100
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %d%%" % ('=' * int(percentage), percentage))
        sys.stdout.flush()

    def create_data_tree(self, benchmark, part, device):
        # Benchmark: original, rt-poll or rt-sse
        if not benchmark in self._data:
            self._data[benchmark] = {}

        # Part of benchmark: liveboard or planner
        if not part in self._data[benchmark]:
            self._data[benchmark][part] = {}

        # Device: jolla-1 or xperia-x
        if not device in self._data[benchmark][part]:
            self._data[benchmark][part][device] = {}

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="LCRail benchmark.")
    parser.add_argument("process",
                        type=str,
                        help="The name of the benchmarked process , for example: <process>-top-<name>.txt")
    args = parser.parse_args()
    process = args.process
    m = Main("results/**/**/**/*.txt", process)
    m.run()

