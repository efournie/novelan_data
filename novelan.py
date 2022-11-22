from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Settings
debug = True
heat_pump_ip = '192.168.1.44'

driver = webdriver.Firefox()
driver.get(f'http://{heat_pump_ip}/Webserver/index.html')

assert 'Heatpump' in driver.title

# Default password is empty, just send return 
elem = driver.find_element(By.ID, 'password_prompt_input')
elem.clear()
elem.send_keys(Keys.RETURN)

# Wait until page is loaded, then navigate to temperatures
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Navigation')))
menu = driver.find_element_by_id('Navigation')
ActionChains(driver).move_to_element(menu).perform()
info = driver.find_element_by_xpath("//ul[@class='nav']/li/a")
ActionChains(driver).move_to_element(info).perform()

# Get list of menu entries, then navigate to the first one ("Temperaturen")
menu_elements = driver.find_elements_by_xpath("//ul[@class='nav']/li/ul/li")
ActionChains(driver).move_to_element(menu_elements[0]).click().perform()

driver.close()
