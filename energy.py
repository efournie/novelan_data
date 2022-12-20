from datetime import datetime
import matplotlib.pyplot as plt

class Energy:
    '''Produced heat energy (kWh) class'''
    def __init__(self, filename):
        self.filename = filename
        self.timestamps = []
        self.values = []
        # load "database" from filename
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for l in lines:
                timestamp = datetime.strptime(l.split(' = ')[0], '%Y-%m-%d %H:%M:%S')
                value = l.split(' = ')[1]
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

    def graph(self, img_filename=''):
        plt.plot(self.timestamps, self.values)
        if img_filename = '':
            plt.show()
        else:
            plt.savefig(img_filename)
