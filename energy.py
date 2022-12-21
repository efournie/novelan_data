import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from novelan import log
class Energy:
    '''Produced heat energy (kWh) class'''
    def __init__(self, filename, ip_address):
        self.filename = filename
        self.ip_address = ip_address
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


    def update_history(self, kWh):
        '''Update the "database"'''
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        self.timestamps.append(now)
        self.values.append(kWh)
        with open(self.filename, 'a') as f:
            f.write(f'{timestamp} = {kWh}\n')


    def usage_since(self, end_timestamp, period_sec=24*3600, error=0.1, filename=''):
        '''Return kWh usage from the given period (in seconds) preceding the timestamp.
        Only periods smaller or equal to period will be taken into consideration.
        The timestamp closest to end_timestamp will be selected as the end timestamp, the
        one closest to this end timestamp - period seconds will be selected as the start 
        timestamp. If the difference between those two timestamps differs by more than
        the given error value from period, an exception is raised.
        If filename is not empty, save the result into this file (overwrite content)
        end_timestamp should be a datetime, period_sec a number of seconds.
        If no suitable start or end timestamp is found, an exception is raised.'''

        # find the a timestamp as close as possible to end_timestamp
        shortest_delta_end = timedelta.max
        for i in range(len(self.timestamps)):
            delta_end = end_timestamp - self.timestamps[i]
            if abs(delta_end.total_seconds()) < abs(shortest_delta_end.total_seconds()):
                shortest_delta_end = delta_end
                end_idx = i
        
        # find a starting timestamp whose delta with the found end timestamp is as close to period as possible
        period_diff_sec = float('inf')
        for i in range(len(self.timestamps)):
            delta_begin = self.timestamps[end_idx] - self.timestamps[i]
            if abs(delta_begin.total_seconds() - period_sec) < period_diff_sec and i != end_idx:
                start_idx = i
                period_diff_sec = abs(delta_begin.total_seconds() - period_sec)

        # Now check if the difference between the two timestamps is close enough to period
        real_period = self.timestamps[end_idx] - self.timestamps[start_idx]
        if abs(period_sec - real_period.total_seconds()) / period_sec > error:
            raise ValueError(f'Error is higher than the maximum allowed : abs({period_sec} - {real_period.total_seconds()}) / {period_sec} > {error}. start_idx={start_idx}, end_idx={end_idx}')
        else:
            usage = self.values[end_idx] - self.values[start_idx]
        
        if filename != '':
            with open(filename, 'w') as f:
                f.write(f'{usage}')
        return usage


    def read_status(self):
        '''Read total energy usage from the heat pump at the given IP address and update
        the file containing the values.
        Unused fields heating, hot_water, total_heatpump, extra and total_kWh are updated.'''
        opts = Options()
        opts.headless = True
        driver = webdriver.Chrome(options=opts)
        driver.get(f'http://{self.ip_address}/Webserver/index.html')
        _ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//html/body')))
        assert 'Heatpump' in driver.title
        # Default password is empty, just send return 
        elem = driver.find_element(By.ID, 'password_prompt_input')
        elem.clear()
        elem.send_keys(Keys.RETURN)

        # Status page
        # Wait until page is loaded, then navigate to energy
        _ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Navigation')))
        menu = driver.find_element_by_id('Navigation')
        ActionChains(driver).move_to_element(menu).perform()
        info = driver.find_element_by_xpath("//ul[@class='nav']/li/a")
        ActionChains(driver).move_to_element(info).perform()
        # Get list of menu entries, then navigate to the 9th one ("Wärmemenge")
        menu_elements = driver.find_elements_by_xpath("//ul[@class='nav']/li/ul/li")
        ActionChains(driver).move_to_element(menu_elements[8]).click().perform()
        _ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'output_field')))
        # Get values
        heat_energies = driver.find_elements(By.CLASS_NAME, 'output_field')
        heat_energies_text = [t.text for t in heat_energies]
        energies_values = [float(t.replace('kWh', '')) 
                                for t in heat_energies_text]
        self.heating = energies_values[0]
        self.hot_water = energies_values[1]
        self.total_heatpump = energies_values[2]
        self.extra = energies_values[3]
        self.total_kWh = energies_values[4]
        driver.close()
        self.update_history(self.total_kWh)


    def debug(self):
        '''Print all timestamps and values contained'''
        for i in range(len(self.timestamps)):
            print(f'{self.timestamps[i]}  :  {self.values[i]}      ({(datetime.now() - self.timestamps[i]).seconds} seconds ago)')

    def lin_graph(self, img_filename=''):
        '''Plot a linear graph of the total energy consumption over time'''
        plt.plot(self.timestamps, self.values)
        if img_filename == '':
            plt.show()
        else:
            plt.savefig(img_filename)

    def graph(self, img_filename=''):
        '''Plot a graph of the energy consumption between all measurement times'''
        vals = []
        for i in range(1, len(self.values)):
            vals.append(self.values[i] - self.values[i-1])
        plt.stairs(vals, self.timestamps, fill=True)
        if img_filename == '':
            plt.show()
        else:
            plt.savefig(img_filename)

def main():
    # Options
    parser = argparse.ArgumentParser(description='Read energy usage of a Novelan heat pump')
    parser.add_argument('-i', '--ip_address', type=str, help='IP address of the heat pump')
    parser.add_argument('-f', '--history_file', type=str, help='Text file where the energy usage will be stored')
    parser.add_argument('-u', '--update', action='store_true', help='Update the file containing the heat pump energy usage')
    parser.add_argument('-d', '--daily_use', type=str, default='', help='Compute the heat pump energy usage for the last 24h and store it into the file given as argument')
    parser.add_argument('-g', '--graph', type=str, default='', help='Generate a bar plot from all the saved values and save it to this file')
    args = parser.parse_args()
    e = Energy(args.history_file, args.ip_address)
    if args.update:
        e.read_status()
    elif args.daily_use != '':
        now = datetime.now()
        e.read_status()
        e.usage_since(now, filename=args.daily_use)
    elif args.graph != '':
        e.graph(args.graph)


if __name__ == '__main__':
    main()