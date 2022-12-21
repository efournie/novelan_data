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
        Only periods smaller or equal to period will be taken into consideration.
        The timestamp closest to end_timestamp will be selected as the end timestamp, the
        one closest to this end timestamp - period seconds will be selected as the start 
        timestamp. If the difference between those two timestamps differs by more than
        the given error value from period, NaN is returned.
        If filename is not empty, save the result into this file (overwrite content)
        end_timestamp should be a datetime, period_sec a number of seconds.
        If no suitable start or end timestamp is found, NaN is returned.'''

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


    def read(self):
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
        self.update(self.total_kWh)


    def debug(self):
        for i in range(len(self.timestamps)):
            print(f'{self.timestamps[i]}  :  {self.values[i]}      ({(datetime.now() - self.timestamps[i]).seconds} seconds ago)')

    def graph(self, img_filename=''):
        plt.plot(self.timestamps, self.values)
        if img_filename == '':
            plt.show()
        else:
            plt.savefig(img_filename)
