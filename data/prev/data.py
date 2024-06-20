import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from country_data import get_country_data

PATH = "D:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(PATH)
driver = webdriver.Chrome(service=service)

main_url = "https://en.wikipedia.org/wiki/List_of_countries"

def save_to_json(data, file_path):
    with open(file_path, 'w+') as json_file:
        json.dump(data, json_file, indent=2)

try:
    driver.get(main_url)
    
    table = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mw-content-ltr"))
    )

    rows = table.find_elements(By.XPATH, ".//tbody/tr")

    data = []
    json_file_path = "./data/dataset/data.json"
    visited_urls = set()
    
    for row in rows:
        table = driver.find_element(By.CLASS_NAME, "mw-content-ltr")
        cell = row.find_element(By.XPATH, ".//td")
        
        try:
            span_element = cell.find_element(By.XPATH, ".//span[1]")
            common_name = span_element.get_attribute('id').replace('_', ' ')
            
            b_element = cell.find_element(By.XPATH, ".//b")
            whole_cell = cell.text
            b_elem_index = whole_cell.find(b_element.text)                
            start_index = b_elem_index + len(b_element.text)
            
            if '\u2013' in whole_cell[start_index:]:
                
                try:
                    ref_element = cell.find_element(By.XPATH, ".//sup").text.strip()
                    main_text = whole_cell.replace(ref_element, '').strip()
                    official_name = main_text[start_index:].strip()
                    official_name = official_name.lstrip('\u2013 ').strip()
                
                except:
                    official_name = whole_cell[start_index:].strip()
                    official_name = official_name.lstrip('\u2013 ').strip()

            else:
                official_name = common_name

        except Exception as e:
            print(e)
            driver.quit()
            
        country_url = b_element.find_element(By.XPATH, ".//a").get_attribute('href')
        
        if country_url in visited_urls:
            continue
        
        country_data = get_country_data(driver, country_url)
        
        # native_names = country_data["native"] if country_data["native"] else {"default": common_name}
        
        if common_name:
            data.append({
                "name": {
                    "common": common_name,
                    "official": official_name,
                    "native": []
                },
                "flag": country_data["flag"],
                "demonyms": [],
                "capital": {
                    "name": "",
                    "location": "",
                    "population": ""
                },
                "languages": {
                    "official": [],
                    "recognised": []
                },
                "ethnic_groups": [
                    {
                        "name": "",
                        "percentage": ""
                    }
                ],
                "religions": [
                    {
                        "name": "",
                        "percentage": ""
                    }
                ],
                "area": {
                    "total": {
                        "km": "0",
                        "mi": "0"
                    },
                    "land": {
                        "km": "0",
                        "mi": "0"
                    },
                    "water_percent": "0"
                }
            })

        # time.sleep(1) # maybe need this breaks too often
        driver.back()
        
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-content-ltr"))
        )
        
        if len(data) % 1 == 0:
            save_to_json(data, json_file_path)

    save_to_json(data, json_file_path)

except Exception as e:
    print(f"whole error: {e}")
    driver.quit()    
finally:
    driver.quit()
    