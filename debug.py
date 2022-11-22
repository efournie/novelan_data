from constants import *

def dbg_temperatures(t):
    print(f'Incoming temp           : {t[t_in]}°C')
    print(f'Outgoing temp           : {t[t_out]}°C')
    print(f'Expected outgoing temp  : {t[t_out_exp]}°C')
    print(f'Hot gas temp            : {t[hot_gas]}°C')
    print(f'Outside temp            : {t[t_ext]}°C')
    print(f'Hot water temp          : {t[t_water]}°C')
    print(f'Expected hot water temp : {t[t_water_exp]}°C')
