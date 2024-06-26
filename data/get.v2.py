from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
from time import sleep
import yaml

PATH = "D:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(PATH)
driver = webdriver.Chrome(service=service)

yaml_file_path = "./dataset/imp.yaml"
json_file_path = "./dataset/data.json"

with open(yaml_file_path, 'r') as yaml_file:
    imp_data = yaml.safe_load(yaml_file)

def load_data(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return data
    
def save_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def process_url(proc_url, data):
    driver.get(proc_url) 
    en_lang = '(English)'
    sleep(2)
    
    body = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
    )
    
    main = body.find_element(By.CLASS_NAME, "wikibase-listview")
    
    common_name = body.find_element(By.CLASS_NAME, "wikibase-title-label").text
    
    official_name = common_name
    try:
        of_name_prop = main.find_element(By.ID, imp_data['properties']['official_name'])
        of_name_rows = of_name_prop.find_elements(By.CLASS_NAME, "listview-item")
        for of_name_row in of_name_rows:
            of_name_item = of_name_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
            of_name_spans = of_name_item.find_elements(By.TAG_NAME, "span")
            if en_lang in of_name_spans[1].text:
                official_name = of_name_spans[0].text
    except:
        pass
    
    native_names = []
    try:
        native_label_prop = main.find_element(By.ID, imp_data['properties']['native_label'])
        native_label_rows = native_label_prop.find_elements(By.CLASS_NAME, "listview-item")
        for native_label_row in native_label_rows:
            native_label_item = native_label_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
            native_label_spans = native_label_item.find_elements(By.TAG_NAME, "span")
            native_label_text = native_label_spans[0].text
            native_names.append(native_label_text)
    except:
        native_names.append(common_name)
    
    population = '0'
    try:
        population_prop = main.find_element(By.ID, imp_data['properties']['population'])
        population_rows = population_prop.find_elements(By.CLASS_NAME, "wb-preferred")
        for population_row in population_rows:
            population = population_row.find_element(By.CLASS_NAME, "wikibase-snakview-value").text
    except:
        pass
    
    continents = []
    try:
        continent_prop = main.find_element(By.ID, imp_data['properties']['continent'])
        continent_items = continent_prop.find_elements(By.CLASS_NAME, "listview-item")
        for continent_item in continent_items:
            continent_text = continent_item.find_element(By.XPATH, './/a').text
            continents.append(continent_text)
    except:
        # continents.append('n/a')
        pass
    
    official_langs = []
    spoken_langs = []
    try:
        of_lang_prop = main.find_element(By.ID, imp_data['properties']['official_lang'])
        of_lang_rows = of_lang_prop.find_elements(By.CLASS_NAME, "listview-item")
        for of_lang_row in of_lang_rows:
            of_lang_text = of_lang_row.find_element(By.XPATH, './/a').text
            official_langs.append(of_lang_text)
        try:
            lang_used_prop = main.find_element(By.ID, imp_data['properties']['lang_used'])
            lang_used_rows = lang_used_prop.find_elements(By.CLASS_NAME, "listview-item")
            for lang_used_row in lang_used_rows:
                lang_used_text = lang_used_row.find_element(By.XPATH, './/a').text
                spoken_langs.append(lang_used_text)
        except:
            spoken_langs = official_langs
    except:
        # official_langs.append('n/a')
        # spoken_langs.append('n/a')
        pass
        
    try:
        # "body"'s here atm cuz its a dif table than "main"
        alpha_2_prop = body.find_element(By.ID, imp_data['properties']['alpha_2_code'])
        alpha_2_rows = alpha_2_prop.find_elements(By.CLASS_NAME, "listview-item")
        for alpha_2_row in alpha_2_rows:
            alpha_2_code = alpha_2_row.find_element(By.CLASS_NAME, "wb-external-id").text
            
        alpha_3_prop = body.find_element(By.ID, imp_data['properties']['alpha_3_code'])
        alpha_3_rows = alpha_3_prop.find_elements(By.CLASS_NAME, "listview-item")
        for alpha_3_row in alpha_3_rows:
            alpha_3_code = alpha_3_row.find_element(By.CLASS_NAME, "wb-external-id").text
        
        numeric_prop = body.find_element(By.ID, imp_data['properties']['numeric_code'])
        numeric_rows = numeric_prop.find_elements(By.CLASS_NAME, "listview-item")
        for numeric_row in numeric_rows:
            numeric_code = numeric_row.find_element(By.CLASS_NAME, "wb-external-id").text
    
    except:
        alpha_2_code, alpha_3_code, numeric_code = ''
    
    data.append({
        "name": {
            "common": common_name,
            "official": official_name,
            "native": native_names
        },
        "population": population,
        "demonym": "demonym",
        "flag": "flag",
        "capital": "capital",
        "continent": continents,
        "languages": {
            "official": official_langs,
            "spoken": spoken_langs
        },
        "code": {
            "alpha-2": alpha_2_code,
            "alpha-3": alpha_3_code,
            "numeric": numeric_code
        },
    })
    save_to_json(data, json_file_path)
    

# data = load_data(json_file_path)
data = []

for place_url in imp_data['place']:
    process_url(place_url, data)

# process_url("https://www.wikidata.org/wiki/Q232")

driver.quit()
