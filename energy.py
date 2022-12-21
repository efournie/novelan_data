from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

class Energy:
    '''Produced heat energy (kWh) class'''
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

    def update(self, kWh):
        '''Update the "database"'''
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        self.timestamps.append(now)
        self.values.append(kWh)
        with open(self.filename, 'a') as f:
            f.write(f'{timestamp} = {kWh}\n')

    def usage_since(self, end_timestamp, period_sec=24*3600, error=0.1, filename=''):
        '''Return kWh usage from the given period (in seconds) preceding the timestamp.
        Note: the first timestamp closer to the input timestamp than the asked period will be 
        taken into consideration. If the difference between those two timestamps differs by more than
        the given error value from period, NaN is returned.
        If filename is not empty, save the result into this file (overwrite content)
        Timestamp should be a datetime'''

        # find the a timestamp as close as possible to end_timestamp
        shortest_delta_end = timedelta.max
        for i in range(len(self.timestamps)):
            # abs() does not work with timedeltas
            if end_timestamp > self.timestamps[i]:
                delta_end = end_timestamp - self.timestamps[i]
            else:
                delta_end = self.timestamps[i] - end_timestamp
            if (delta_end) < shortest_delta_end:
                shortest_delta_end = delta_end
                end_idx = i
        
        # find the first timestamp whose delta with the found end timestamp is shorter or equal to period
        start_idx = -1
        for i in range(len(self.timestamps)):
            delta_begin = self.timestamps[end_idx] - self.timestamps[i]
            if delta_begin.seconds <= period_sec:
                start_idx = i
                break
        if start_idx == -1:
            # There is no delta <= period 
            usage = float('NaN')
            if filename != '':
                with open(filename, 'w') as f:
                    f.write(f'{usage}')
            return usage

        # Now check if the difference between the two timestamps is close enough to period
        real_period = self.timestamps[end_idx] - self.timestamps[start_idx]
        if (period_sec - real_period.seconds) / period_sec > error:
            usage = float('NaN')
        else:
            usage = self.values[end_idx] - self.values[start_idx]
        
        if filename != '':
            with open(filename, 'w') as f:
                f.write(f'{usage}')
        return usage


    def debug(self):
        for i in range(len(self.timestamps)):
            print(f'{self.timestamps[i]}  :  {self.values[i]}      ({(datetime.now() - self.timestamps[i]).seconds} seconds ago)')

    def graph(self, img_filename=''):
        plt.plot(self.timestamps, self.values)
        if img_filename == '':
            plt.show()
        else:
            plt.savefig(img_filename)
