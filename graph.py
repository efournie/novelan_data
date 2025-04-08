import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import os

class Graph:
    def __init__(self, filename, filename2='', filter_len=35, monotonous=False):
        self.filename = filename
        self.filename2 = filename2
        self.filter_len = filter_len
        self.timestamps = []
        self.values = []
        self.timestamps2 = []
        self.values2 = []
        self.double = False
        self.name1 = os.path.basename(filename).split('.')[0].replace('hist_', '')
        self.name2 = os.path.basename(filename2).split('.')[0].replace('hist_', '')
        # load "database" from filename
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for l in lines:
                    timestamp = datetime.strptime(l.split(' = ')[0], '%Y-%m-%d %H:%M:%S')
                    value = float(l.split(' = ')[1].replace('\n', ''))
                    self.timestamps.append(timestamp)
                    self.values.append(value)
        if filename2 != '' and os.path.exists(self.filename2):
            with open(self.filename2, 'r') as f:
                lines = f.readlines()
                for l in lines:
                    timestamp = datetime.strptime(l.split(' = ')[0], '%Y-%m-%d %H:%M:%S')
                    value = float(l.split(' = ')[1].replace('\n', ''))
                    self.timestamps2.append(timestamp)
                    self.values2.append(value)
            self.double = True
        if monotonous:
            self.convert_monotonous()

    def convert_monotonous(self):
        v0 = self.values[0]
        ts2 = []
        val2 = []
        for i in range(1, len(self.values)):
            value_diff = self.values[i] - self.values[i-1]
            hours_between_values = (self.timestamps[i] - self.timestamps[i-1]).total_seconds() * 3600
            if hours_between_values > 0 and value_diff > 0:
                ts2.append(self.timestamps[i])
                val2.append(value_diff / hours_between_values)
        self.values = val2
        self.timestamps = ts2

    def split_years(self, timestamps, values):
        ts2 = []
        val2 = []
        current_year = timestamps[0].year
        ts_cur_year = []
        val_cur_year = []
        idx = 0
        for d in timestamps:
            if d.year == current_year:
                ts_cur_year.append(timestamps[idx])
                val_cur_year.append(values[idx])
            else:
                ts2.append(ts_cur_year)
                val2.append(val_cur_year)
                ts_cur_year = [timestamps[idx]]
                val_cur_year = [values[idx]]
                current_year = d.year
            idx += 1
        ts2.append(ts_cur_year)
        val2.append(val_cur_year)
        return ts2, val2

    def filter(self, x):
        filt_val = []
        for idx in range(len(x)):
            i0 = max(0, idx - self.filter_len // 2)
            i1 = min(len(x), idx + self.filter_len // 2)
            l = i1 - i0
            val = 0
            for idx2 in range(i0, i1):
                val += x[idx2]
            val = val / l
            filt_val.append(val)
        return filt_val

    def graph(self, img_filename='', filter=False, yearly=False, graph_days=-1, width=12):
        '''Plot a graph of the energy consumption between all measurement times'''
        if filter:
            self.values = self.filter(self.values)

        if graph_days == -1:
            timestamps = self.timestamps
            values = self.values
            if self.double:
                timestamps2 = self.timestamps2
                values2 = self.values2
        else:
            timestamps = [i for i in self.timestamps if self.timestamps[-1] - i <= timedelta(days=graph_days)]
            values = self.values[ -len(timestamps): ]
            if self.double:
                timestamps2 = [i for i in self.timestamps2 if self.timestamps2[-1] - i <= timedelta(days=graph_days)]
                values2 = self.values2[ -len(timestamps2): ]

        if not yearly:
            plt.figure(figsize=(width, width/2.4))
            if self.double:
                plt.plot(timestamps2, values2, 'r', label=self.name2)
            ax = plt.plot(timestamps, values, 'b', label=self.name1)
            plt.grid(True, 'both', 'y')
        else:
            split_ts, split_vals = self.split_years(timestamps, values)
            last_year = split_ts[-1][0].year
            for timestamps, values in zip(split_ts, split_vals):
                year = timestamps[0].year
                new_timestamps = []
                for idx in range(len(timestamps)):
                    t = timestamps[idx]
                    t2 = datetime(last_year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond)
                    new_timestamps.append(t2)
                ax = plt.plot(new_timestamps, values, label=f'{year}')

        plt.legend()
        if img_filename == '':
            plt.show()
        else:
            plt.savefig(img_filename)

def main():
    # Options
    parser = argparse.ArgumentParser(description='Generate a graph from a file containing timestamps and values')
    parser.add_argument('-f', '--history_file', type=str, help='File where the timestamps and values are stored')
    parser.add_argument('--f2', type=str, default='', help='Second values file (optional)')
    parser.add_argument('-g', '--graph', type=str, default='', help='Generate a graph from the saved values and save it to this file')
    parser.add_argument('--graph_days', type=int, default=-1, help='Limit the graph to the last N days. No effect if -g is not set.')
    parser.add_argument('--graph_width', type=int, default=12, help='Width of the graph in inches.')
    parser.add_argument('-y', '--yearly', action='store_true', help='Superimpose yearly graphs.')
    parser.add_argument('--filter', action='store_true', help='Smooth the graphs.')
    parser.add_argument('--filter_len', type=int, default=35, help='Length of the filter.')
    parser.add_argument('--monotonous', action='store_true', help='Values are monotonously increasing, first convert them to differences between consecutive values.')
    args = parser.parse_args()
    e = Graph(args.history_file, args.f2, args.filter_len, args.monotonous)
    e.graph(args.graph, args.filter, args.yearly, args.graph_days, args.graph_width)


if __name__ == '__main__':
    main()

