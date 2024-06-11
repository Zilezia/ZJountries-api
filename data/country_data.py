from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_country_data(driver, country_url):
    driver.get(country_url)
    
    try:
        main = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
        )
        common_name = main.find_element(By.CLASS_NAME, "mw-page-title-main").text
        
        try:
            official_name = main.find_element(By.CLASS_NAME, "country-name").text
        except:
            official_name = common_name
        
        try:
            native_names_box = main.find_element(By.CLASS_NAME, "ib-country-names")
            names_list = native_names_box.find_elements(By.XPATH, ".//span[@title]")
            native_names = [name.text for name in names_list]
        except:
            native_names = common_name
        
        print(f"country: {common_name}")
    
    except Exception as e:
        print(f"error fetching {country_url}: {e}")
        
    country_data = {
        "common": common_name,
        "official": official_name,
        "native": native_names
    }
    return country_data