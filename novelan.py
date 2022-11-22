import argparse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from temperatures import Temperatures


def main():
    # Options
    parser = argparse.ArgumentParser(description='Read status of a Novelan heat pump')
    parser.add_argument('-i', '--ip_address', type=str, help='IP address of the heat pump')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='Output directory where CSV files will be written')
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode, print results')
    args = parser.parse_args()

    # Login page
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    driver.get(f'http://{args.ip_address}/Webserver/index.html')
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
    temps = Temperatures(temperatures_values)

    if args.debug:
        temps.debug()

    temps.write_all(args.output_dir)

    driver.close()


if __name__ == '__main__':
    main()