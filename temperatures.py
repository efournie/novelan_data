import os

class Temperature:
    '''Single temperature class'''
    def __init__(self, name, value=float('nan')):
        self.name = name
        self.value = value

    def write_csv(self, filename):
        '''Write temperature value in a CSV file'''
        with open(filename, 'a') as f:
            f.write(f'{self.value} ,')

    def write_value(self, filename):
        '''Write current temperature value in a file. Contents of the file will be overwritten.'''
        with open(filename, 'w') as f:
            f.write(f'{self.value}')


class HeatPumpStatus():
    '''Global heat pump status class'''
    def __init__(self, temps):
        self.t_in = Temperature('Flow temperature', temps[0])
        self.t_out = Temperature('Return temperature', temps[1])
        self.t_out_exp = Temperature('Expected return temperature', temps[2])
        self.t_out_ext = Temperature('Outside return temperature', temps[3])
        self.hot_gas = Temperature('Hot gas', temps[4])
        self.t_ext = Temperature('Outside temperature', temps[5])
        self.mid_temp = Temperature('Average temperature', temps[6])
        self.t_water = Temperature('Hot water temperature', temps[7])
        self.t_water_exp = Temperature('Expected hot wated temperature', temps[8])
        self.heat_source_in = Temperature('Heat source incoming temperature', temps[9])
        self.t_in_max = Temperature('Maximum flow temperature', temps[10])
        self.overheat = Temperature('Overheat', temps[12])
        self.overheat_exp = Temperature('Expected overheat', temps[13])
        self.t_condensation = Temperature('Condensation temperature', temps[18])

    def debug(self):
        values = self.__dict__
        for t in values:
            print(f'{values[t].name} : {values[t].value}°C')

    def write_all(self, dir):
        values = self.__dict__
        for t in values:
            filename = os.path.join(dir, f'{t}.csv')
            values[t].write_csv(filename)
            filename = os.path.join(dir, f'{t}.temp')
            values[t].write_value(filename)
