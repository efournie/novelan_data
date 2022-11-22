from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Firefox()
driver.get("http://192.168.1.44/Webserver/index.html")
assert "Heatpump" in driver.title

elem = driver.find_element(By.ID, "password_prompt_input")
elem.clear()
elem.send_keys(Keys.RETURN)

time.sleep(1)

menu = driver.find_element_by_id('Navigation')
ActionChains(driver).move_to_element(menu).perform()

info = driver.find_element_by_xpath("//ul[@class='nav']/li/a")
ActionChains(driver).move_to_element(info).perform()

menu_elements = driver.find_elements_by_xpath("//ul[@class='nav']/li/ul/li")
ActionChains(driver).move_to_element(menu_elements[0]).click().perform()
# ActionChains(driver).move_to_element(menu).move_to_element(info).move_to_element(menu_elements[0]).click().perform()


driver.close()
