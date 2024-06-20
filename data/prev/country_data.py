from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def get_country_data(driver, url):
    driver.get(url)
    
    try:
        body = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
        )

        try:
            flag_element = body.find_element(By.XPATH, ".//tr/td/div/div/div/span/a")

        except:
            flag_element = body.find_element(By.XPATH, ".//tr/td/div/div/span/a")

        flag_element.click()
        
        
        flag_zoom_e = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-mmv-wrapper"))
        )
        time.sleep(1)
        
        flag = flag_zoom_e.find_element(By.CLASS_NAME, "mw-mmv-final-image").get_attribute('src')
        
        driver.back()
        
    except Exception as e:
        print(f"error fetching country name: {e}")
        
    country_data = {
        "flag": flag,
}
    return country_data