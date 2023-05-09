import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import os

class Graph:
    def __init__(self, filename, filename2=''):
        self.filename = filename
        self.filename2 = filename2
        self.timestamps = []
        self.values = []
        self.timestamps2 = []
        self.values2 = []
        self.double = False
        self.name1 = os.path.basename(filename).split('.')[0]
        self.name2 = os.path.basename(filename2).split('.')[0]
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

    def graph(self, img_filename=''):
        '''Plot a graph of the energy consumption between all measurement times'''
        vals = []
        ts = []
        filt_len = 11
        plt.figure(figsize=(16,6))
        plt.plot(self.timestamps, self.values, 'b', label=self.name1)
        if self.double:
            plt.plot(self.timestamps2, self.values2, 'r', label=self.name2)
        plt.grid(True, 'both', 'y')
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
    args = parser.parse_args()
    e = Graph(args.history_file, args.f2)
    if args.graph != '':
        e.graph(args.graph)


if __name__ == '__main__':
    main()
