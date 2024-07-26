from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
from time import sleep

PATH = "D:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(PATH)
driver = webdriver.Chrome(service=service)

json_file_path = "./data/dataset/natn.json" # save file

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
    
    body = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mw-body-content"))
    )
    sleep(1)
    table = body.find_element(By.CLASS_NAME, "infobox")
    
    native_names = {}
    try:
        nat_names_row = table.find_element(By.CLASS_NAME, "ib-settlement-native")
        
        try:
            more_spans = nat_names_row.find_element(By.XPATH, ".//span")
        except:
            more_spans = None
            
        if more_spans:
            native_names["cap_natn"] = more_spans.text
        else:
            native_names["cap_natn"] = nat_names_row.text
        
    except Exception as e:
        print("Error: ", e)
        driver.quit()
        return
    

    data.append({
        
        "native_name": native_names
        
    })
    save_to_json(data, json_file_path)
    
data = []

capital_url = "https://en.wikipedia.org/wiki/warsaw"
# capital_url = "https://en.wikipedia.org/wiki/pristina"
# capital_url = "https://en.wikipedia.org/wiki/kabul"

process_url(capital_url, data)

driver.quit()
