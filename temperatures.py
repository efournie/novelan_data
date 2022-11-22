class Temperature:
    def __init__(self, name, value=float('nan')):
        self.name = name
        self.value = value
        

class Temperatures():
    def __init__(self, temps):
        self.t_in = Temperature('Incoming temperature', temps[0])
        self.t_out = Temperature('Outgoing temperature', temps[1])
        self.t_out_exp = Temperature('Expected outgoing temperature', temps[2])
        self.t_out_ext = Temperature('Outside outgoing temperature', temps[3])
        self.hot_gas = Temperature('Hot gas', temps[4])
        self.t_ext = Temperature('Outside temperature', temps[5])
        self.mid_temp = Temperature('Average temperature', temps[6])
        self.t_water = Temperature('Hot water temperature', temps[7])
        self.t_water_exp = Temperature('Expected hot wated temperature', temps[8])
        self.heat_source_in = Temperature('Heat source incoming temperature', temps[9])
        self.t_in_max = Temperature('Maximum input temperature', temps[10])
        self.overheat = Temperature('Overheat', temps[12])
        self.overheat_exp = Temperature('Expected overheat', temps[13])
        self.t_condensation = Temperature('Condensation temperature', temps[18])

    def debug(self):
        values = self.__dict__
        for t in values:
            print(f'{values[t].name} : {values[t].value}°C')
