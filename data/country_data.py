from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_country_data(driver, url):
    driver.get(url)
    
    try:
        body = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
        )
            
        # flag_page = body.find_element(By.XPATH, ".//tr/td/div/div/div/span/a").get_attribute('href')
        # driver.get(flag_page)
        
        # try:
        #     body = WebDriverWait(driver, 50).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "mw-body-content"))
        #     )
            
        #     flag = body.find_element(By.XPATH, ".//div/a/img").get_attribute('src')
            
        #     driver.back()
        
        # except:
        #     flag = 'N/A'
        
        # demonym_row = body.find_element(By.XPATH, ".//tr/th/a[@title]")
        # if 'Demonym(s)' in demonym_row.text:
        #     demonyms = demonym_row.find_element(By.XPATH, './td/a').text
        
    except Exception as e:
        print(f"error fetching country name: {e}")
        
    country_data = {
        # "native": native_names,
        # "flag": flag,
        # "demonyms": demonyms
}
    return country_data