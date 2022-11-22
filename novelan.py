from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from constants import *
from debug import dbg_temperatures

# Settings
heat_pump_ip = '192.168.1.44'
debug = True

# Login page
driver = webdriver.Firefox()
driver.get(f'http://{heat_pump_ip}/Webserver/index.html')
_ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//html/body')))
assert 'Heatpump' in driver.title
# Default password is empty, just send return 
elem = driver.find_element(By.ID, 'password_prompt_input')
elem.clear()
elem.send_keys(Keys.RETURN)

# Status page
# Wait until page is loaded, then navigate to temperatures
_ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Navigation')))
menu = driver.find_element_by_id('Navigation')
ActionChains(driver).move_to_element(menu).perform()
info = driver.find_element_by_xpath("//ul[@class='nav']/li/a")
ActionChains(driver).move_to_element(info).perform()
# Get list of menu entries, then navigate to the first one ("Temperaturen")
menu_elements = driver.find_elements_by_xpath("//ul[@class='nav']/li/ul/li")
ActionChains(driver).move_to_element(menu_elements[0]).click().perform()
_ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'output_field')))

# Temperatures
# Get values
temperatures = driver.find_elements(By.CLASS_NAME, 'output_field')
temperatures_text = [t.text for t in temperatures]
temperatures_values = [float(t.replace('°C', '').replace('°F', '').replace(' K', '')) 
                        for t in temperatures_text]

if debug:
    dbg_temperatures(temperatures_values)

driver.close()
