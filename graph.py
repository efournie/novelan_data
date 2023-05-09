import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import os

class Graph:
    def __init__(self, filename):
        self.filename = filename
        self.timestamps = []
        self.values = []
        # load "database" from filename
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for l in lines:
                    timestamp = datetime.strptime(l.split(' = ')[0], '%Y-%m-%d %H:%M:%S')
                    value = float(l.split(' = ')[1].replace('\n', ''))
                    self.timestamps.append(timestamp)
                    self.values.append(value)

    def graph(self, img_filename=''):
        '''Plot a graph of the energy consumption between all measurement times'''
        vals = []
        ts = []
        filt_len = 11
        plt.figure(figsize=(16,6))
        plt.plot(self.timestamps, self.values)
        plt.grid(True, 'both', 'y')
        if img_filename == '':
            plt.show()
        else:
            plt.savefig(img_filename)

def main():
    # Options
    parser = argparse.ArgumentParser(description='Read energy usage of a Novelan heat pump')
    parser.add_argument('-f', '--history_file', type=str, help='Text file where the energy usage will be stored')
    parser.add_argument('-g', '--graph', type=str, default='', help='Generate a bar plot from all the saved values and save it to this file')
    args = parser.parse_args()
    e = Graph(args.history_file)
    if args.graph != '':
        e.graph(args.graph)


if __name__ == '__main__':
    main()
