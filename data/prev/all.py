import json
from time import sleep
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

def load_data(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        visited_place = {entry['name']['common'] for entry in data}
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
        visited_place = set()
    return data, visited_place

def save_to_json(data, file_path):
    with open(file_path, 'w+') as json_file:
        json.dump(data, json_file, indent=2)


def process_url(url, data, visited_place):
    driver.get(url) 
    sleep(3)
    try:
        main = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wikibase-listview"))
        )
        try:
            prop_527 = main.find_element(By.ID, "P527")
            has_parts = prop_527.find_elements(By.CLASS_NAME, "listview-item")
        except:
            pass
        try:
            prop_31 = main.find_element(By.ID, "P31")
            instances_of = prop_31.find_elements(By.CLASS_NAME, "listview-item")
        except:
            pass

        regions = ('continent', 'geographic region', 'part of the world')
        places = ('country', 'sovereign state', 'autonomous administrative territorial entity', 'dependent territory', 'state')

        try:
            for instance_of in instances_of:
                instance = instance_of.find_element(By.XPATH, './/a')
                instance_text = instance.text.lower()
                
                if has_parts:
                    for has_part in has_parts:
                        
                        if 'continent' in instance_text:
                            next_url = has_part.find_element(By.XPATH, './/a').get_attribute('href')
                            process_url(next_url, data, visited_place)
                        
                        elif 'geographic region' in instance_text:
                            next_url = has_part.find_element(By.XPATH, './/a').get_attribute('href')
                            process_url(next_url, data, visited_place)
                        
                        elif any(place in instance_text for place in places):
                            # try:
                            #     country_data = get_country_data(driver)
                            #     common_name = country_data['common_name']
                            #     if common_name not in visited_place:
                            #         data.append({
                            #             "name": {
                            #                 "common": common_name
                            #                 # "official": country_data['official_name'],
                            #                 # "native": country_data['common_name'],
                            #                 # "other": country_data['common_name']
                            #             }
                            #         })
                            #         save_to_json(data, json_file_path)
                            #         sleep(1)
                            #         visited_place.add(common_name)
                                    
                            #     return driver.back()
                                
                            # except Exception as e:
                            #     print(f'place error: {e}')
                            #     driver.quit()
                            return driver.quit()
                                    
                else:
                    # if any(place in instance_text for place in places):
                    #     country_data = get_country_data(driver)
                    #     common_name = country_data['common_name']
                    #     if common_name not in visited_place:
                    #         data.append({
                    #             "name": {
                    #                 "common": common_name
                    #                 # "official": country_data['official_name'],
                    #                 # "native": country_data['common_name'],
                    #                 # "other": country_data['common_name']
                    #             }
                    #         })
                    #         save_to_json(data, json_file_path)
                    #         sleep(1)
                    #         visited_place.add(common_name)
                    #     return driver.back()
                    return driver.quit()
            
            return driver.back()
                    
        except Exception as e:
            print(f'fors error: {e}')
            return driver.quit()
            
    except Exception as e:
        print(f'error: {e}')
        driver.quit()
        
data, visited_place = load_data(json_file_path)        

for url in continent_url_list:
    process_url(url, data, visited_place)

driver.quit()
