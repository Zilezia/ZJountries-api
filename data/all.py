import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from get import get_country_data

PATH = "D:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(PATH)
driver = webdriver.Chrome(service=service)

continent_url_list = [
    "https://www.wikidata.org/wiki/Q46",
    "https://www.wikidata.org/wiki/Q15",
    "https://www.wikidata.org/wiki/Q49",
    "https://www.wikidata.org/wiki/Q18",
    "https://www.wikidata.org/wiki/Q48",
    "https://www.wikidata.org/wiki/Q55643",
    "https://www.wikidata.org/wiki/Q51"
]

json_file_path = "./data/dataset/data.json"
data = []
visited_urls = set()

def save_to_json(data, file_path):
    with open(file_path, 'w+') as json_file:
        json.dump(data, json_file, indent=2)

def process_url(url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    driver.get(url)
    try:
        time.sleep(5)
        main = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wikibase-listview"))
        )
        try:
            prop_31 = main.find_element(By.ID, "P31")
            parts = prop_31.find_elements(By.CLASS_NAME, "listview-item")
            
            for part in parts:
                item = part.find_element(By.XPATH, './/a')
                item_url = item.get_attribute('href')
                if 'continent' in item.text.lower():
                    try:
                        has_parts = main.find_element(By.ID, "P527")
                        sub_parts = has_parts.find_elements(By.CLASS_NAME, "listview-item")
                        for sub_part in sub_parts:
                            next_url = sub_part.find_element(By.XPATH, './/a').get_attribute('href')
                            process_url(next_url)
                    except Exception as e:
                        print(f"has_parts error: {e}")
                        driver.back()
        except:
            print("not a continent")
            # process_url(url)

    except Exception as e:
        print(f"error processing: {e}")
        driver.quit()
                
for url in continent_url_list:
    process_url(url)

        # continent_row = main.find_element(By.ID, "P527")
        
        # country_url = cell.find_element(By.XPATH, ".//a").get_attribute('href')
        
        # country_data = get_country_data(driver, country_url)
        
        # data.append({
        #     "name": {
        #         "common": country_data["common_name"],
        #         "official": country_data["official_name"],
        #         "native": country_data["native_names"],
        #         "other": ""
        #     },
        #     "flag": country_data["flag"],
        #     "population": country_data["population"],
        #     "demonyms": [],
        #     "capital": {
        #         "name": "",
        #         "location": "",
        #         "population": ""
        #     },
        #     "languages": [],
        #     "ethnic_groups": [
        #         {
        #             "name": "",
        #             "percentage": ""
        #         }
        #     ],
        #     "religions": [
        #         {
        #             "name": "",
        #             "percentage": ""
        #         }
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

        # WebDriverWait(driver, 50).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "wikibase-listview"))
        # )
        
        # if len(data) % 1 == 0:
        #     save_to_json(data, json_file_path)

        # save_to_json(data, json_file_path)

driver.quit()
