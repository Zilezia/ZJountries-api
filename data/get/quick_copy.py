# ZJountries-api is a RESTful program indented for quick access to world places data
# Copyright (C) 2024  Zilezia
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import yaml

PATH = "D:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(PATH)
driver = webdriver.Chrome(service=service)

yaml_file_path = "./copy_test.yaml"

def read_yaml(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file) or {}
    except FileNotFoundError:
        return {}

def save_to_yaml(file_path, data):
    with open(file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

def append_to_place(part_url):
    data = read_yaml(yaml_file_path)
    if 'place' not in data:
        data['place'] = []
    if part_url not in data['place']:
        data['place'].append(part_url)
    save_to_yaml(yaml_file_path, data)

def process_url(proc_url):
    driver.get(proc_url) 
    sleep(2)
    main = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wikibase-listview"))
    )
    prop_527 = main.find_element(By.ID, "P527")
    has_parts = prop_527.find_elements(By.CLASS_NAME, "listview-item")
    
    for has_part in has_parts:
        has_part_url = has_part.find_element(By.XPATH, './/a').get_attribute('href')
        sleep(2)
        append_to_place(has_part_url)
    
with open('grouped.txt', 'r') as file:
    url_list = [line.strip() for line in file if line.strip()]
    
for url_item in url_list:
    process_url(url_item)

driver.quit()
