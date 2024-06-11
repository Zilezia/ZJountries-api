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
    json_file_path = "./data/data.json"
    retry_attempts = 3
    visited_urls = set()
    
    for row in rows:
        table = driver.find_element(By.CLASS_NAME, "mw-content-ltr")
        country_elements = row.find_elements(By.XPATH, ".//td/b/a")
        
        if not country_elements:
            continue
        
        country = country_elements[0]
        country_name = country.text
        country_url = country.get_attribute('href')
        
        if country_url in visited_urls:
            continue
        
        print(country_url)
        
        country_data = get_country_data(driver, country_url)
        
        if country_data:
            data.append({
                "name": {
                    "common": country_data["common"],
                    "official": country_data["official"],
                    "native": country_data["native"]
                }
            })
            # data.append({
            #     "name": {
            #         "common": country_data["common_name"],
            #         "official": country_data["official_name"],
            #         "native": [] # name/s in countrys official language/s
            #     },
            #     "population": "", # maybe add list of population by date/years
            #     "flag": "", # svg flag link
            #     "capital": {
            #         "name": "",
            #         "location": "", # geohack link,
            #         "population": ""
            #     },
            #     "languages": {
            #         "official": [], # official language/s spoken
            #         "recognised": [] # recognised language/s spoken typically in that country
            #     },
            #     "denonyms": [],
            #     "ethnic_groups": [
            #         # {
            #         #     "name": "name",
            #         #     "percentage": "%"
            #         # }
            #     ],
            #     "religions": [
            #         # {
            #         #     "name": "name",
            #         #     "percentage": "%"
            #         # }
            #     ],
            #     "area": {
            #         "total": {
            #             "km": "0",
            #             "mi": "0"
            #         },
            #         "land": {
            #             "km": "0",
            #             "mi": "0"
            #         },
            #         "water_percent": "0"
            #     }
            # })
            visited_urls.add(country_url) # so that wouldnt have duplicates

        time.sleep(1) # maybe need this breaks too often
        driver.back()
        
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-content-ltr"))
        )
        
        if len(data) % 1 == 0:
            save_to_json(data, json_file_path)

    save_to_json(data, json_file_path) 

except Exception as e:
    print(f"error: {e}")
    
finally:
    driver.quit()
    