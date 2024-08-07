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

import json
from time import sleep
import yaml

PATH = "D:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(PATH)
driver = webdriver.Chrome(service=service)

yaml_file_path = "./data/dataset/imp.yaml" # important for scraping data from wikidata
json_file_path = "./data/dataset/td.json" # save file

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
    
    prop = imp_data['properties']
    
    body = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
    )
    sleep(1)
    main = body.find_element(By.CLASS_NAME, "wikibase-listview")
    
    common_name = body.find_element(By.CLASS_NAME, "wikibase-title-label").text
    
    official_name = common_name
    try:
        of_name_prop = main.find_element(By.ID, prop['official_name'])
        of_name_rows = of_name_prop.find_elements(By.CLASS_NAME, "listview-item")
        for of_name_row in of_name_rows:
            of_name_item = of_name_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
            of_name_spans = of_name_item.find_elements(By.TAG_NAME, "span")
            if en_lang in of_name_spans[1].text:
                official_name = of_name_spans[0].text
    except:
        pass
    
    if common_name == official_name and 'Republic of' in common_name:
        common_name = common_name.replace('Republic of', '').strip()
      
    population = "0"
    try:
        population_prop = main.find_element(By.ID, prop['population'])
        population_row = population_prop.find_elements(By.CLASS_NAME, "wb-preferred")
        population = population_row[0].find_element(By.CLASS_NAME, "wikibase-snakview-value").text
    except:
        pass
    
    demonyms = []
    try:
        demonyms_prop = main.find_element(By.ID, prop['demonyms'])
        demonyms_rows = demonyms_prop.find_elements(By.CLASS_NAME, "listview-item")
        for demonyms_row in demonyms_rows:
            demonyms_item = demonyms_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
            demonyms_spans = demonyms_item.find_elements(By.TAG_NAME, "span")
            if en_lang in demonyms_spans[1].text:
                demonyms_text = demonyms_spans[0].text
                demonyms.append(demonyms_text)
        if demonyms_text not in demonyms:
            demonyms.append(f"From {common_name}")
    except:
        demonyms.append(f"From {common_name}")
    
    continents = []
    try:
        continent_prop = main.find_element(By.ID, prop['continent'])
        continent_items = continent_prop.find_elements(By.CLASS_NAME, "listview-item")
        for continent_item in continent_items:
            continent_text = continent_item.find_element(By.XPATH, './/a').text
            continents.append(continent_text)
    except:
        pass
    # maybe not include
    a_part_of = []
    try:
        part_of_prop = main.find_element(By.ID, prop['part_of'])
        part_of_items = part_of_prop.find_elements(By.CLASS_NAME, "listview-item")
        for part_of_item in part_of_items:
            part_of_text = part_of_item.find_element(By.XPATH, './/a').text
            a_part_of.append(part_of_text)
    except:
        pass
    
    official_langs = []
    spoken_langs = []
    try:
        of_lang_prop = main.find_element(By.ID, prop['official_lang'])
        of_lang_rows = of_lang_prop.find_elements(By.CLASS_NAME, "listview-item")
        for of_lang_row in of_lang_rows:
            of_lang_text = of_lang_row.find_element(By.XPATH, './/a').text
            official_langs.append(of_lang_text)
        
        try:
            lang_used_prop = main.find_element(By.ID, prop['lang_used'])
            lang_used_rows = lang_used_prop.find_elements(By.CLASS_NAME, "listview-item")
            for lang_used_row in lang_used_rows:
                lang_used_text = lang_used_row.find_element(By.XPATH, './/a').text
                spoken_langs.append(lang_used_text)
        except:
            spoken_langs = official_langs
    except:
        pass
    
    total_area = {"km":"0", "mi":"0"}
    water_perc = "0"
    total_land_area = {"km":"0", "mi":"0"}
    try:

        try:
            water_perc_prop = main.find_element(By.ID, prop['water_perc'])
        except:
            water_perc_prop = None
        
        if water_perc_prop != None:
            water_perc_prop = main.find_element(By.ID, prop['water_perc'])
            water_perc_row = water_perc_prop.find_elements(By.CLASS_NAME, "listview-item")
            water_perc_text = water_perc_row[0].find_element(By.CLASS_NAME, "wikibase-snakview-value").text
        
            water_perc = water_perc_text.replace(" percent", "")

            water_perc_num = float(water_perc)
        
        try:
            total_area_prop = main.find_element(By.ID, prop['total_area'])
        except:
            total_area_prop = None
        
        if total_area_prop != None:
            total_area_prop = main.find_element(By.ID, prop['total_area'])
            total_area_row = total_area_prop.find_elements(By.CLASS_NAME, "listview-item")
            total_area_text = total_area_row[0].find_element(By.CLASS_NAME, "wikibase-snakview-value").text
            total_area_strip = total_area_text.replace(" square kilometre", "").replace(",", '')
            
            ta_km = int(total_area_strip)

            ta_mi = round(ta_km/1.609344)

            formatted_km = str('{:,}'.format(ta_km))
            formatted_mi = str('{:,}'.format(ta_mi))

            if (ta_km or ta_mi) != "0" and water_perc_num == "0":
                total_land_area["km"], total_area["km"] = formatted_km, formatted_km
                total_land_area["mi"], total_area["mi"] = formatted_mi, formatted_mi

            elif (ta_km or ta_mi) != "0" and water_perc_num != "0":
                tla_km = round(ta_km - (water_perc_num*ta_km)/100)
                tla_mi = round(ta_mi - (water_perc_num*ta_mi)/100)

                total_land_area["km"] = str('{:,}'.format(tla_km))
                total_land_area["mi"] = str('{:,}'.format(tla_mi))
            
    except:
        pass
    
    alpha_2_code=''
    alpha_3_code=''
    numeric_code=''
    subdiv_code =''
    try:
        # "body"'s here atm cuz its a dif table than "main"
        alpha_2_prop = body.find_element(By.ID, prop['alpha_2_code'])
        alpha_2_rows = alpha_2_prop.find_elements(By.CLASS_NAME, "listview-item")
        try:
            alpha_2_code = alpha_2_rows[0].find_element(By.CLASS_NAME, "wb-external-id").text
        except:
            alpha_2_code = alpha_2_rows[1].find_element(By.CLASS_NAME, "wb-external-id").text
        
        alpha_3_prop = body.find_element(By.ID, prop['alpha_3_code'])
        alpha_3_rows = alpha_3_prop.find_elements(By.CLASS_NAME, "listview-item")
        try:
            alpha_3_code = alpha_3_rows[0].find_element(By.CLASS_NAME, "wb-external-id").text
        except:
            alpha_3_code = alpha_3_rows[1].find_element(By.CLASS_NAME, "wb-external-id").text
        
        numeric_prop = body.find_element(By.ID, prop['numeric_code'])
        numeric_rows = numeric_prop.find_elements(By.CLASS_NAME, "listview-item")
        try:
            numeric_code = numeric_rows[0].find_element(By.CLASS_NAME, "wb-external-id").text
        except:
            numeric_code = numeric_rows[1].find_element(By.CLASS_NAME, "wb-external-id").text
        try:
            subdiv_prop = body.find_element(By.ID, prop['subdiv_code'])
            subdiv_rows = subdiv_prop.find_elements(By.CLASS_NAME, "wb-preferred")
            subdiv_code = subdiv_rows[0].find_element(By.CLASS_NAME, "wb-external-id").text
        except:
            subdiv_code = alpha_2_code
    except:
        pass
    
    # Scraped elements that need to go to other ur
    
    # moved down cuz bugged the whole thing
    native_names = {}
    try:
        driver.get(f"https://en.wikipedia.org/wiki/{common_name}") 
        
        
        body = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body-content"))
        )
        sleep(1)
        table = body.find_element(By.CLASS_NAME, "infobox")
        nat_names_row = table.find_element(By.CLASS_NAME, "ib-country-names")
        # Testing it out this way, works kinda better than before 
        try:
            plainlist_div = nat_names_row.find_element(By.XPATH, ".//div[@class='plainlist']")
        except:
            plainlist_div = None
        
        if plainlist_div:
            nat_names_list = nat_names_row.find_elements(By.XPATH, ".//ul/li")
            for nat_name_item in nat_names_list:
                nat_name = nat_name_item.find_element(By.XPATH, ".//span[1]").text # idk how to find by title it errors out
                lang_text = nat_name_item.find_element(By.XPATH, ".//span[@class='languageicon']").text
                nat_lang = lang_text.replace('(', '').replace(')', '').lower()
                native_names[nat_lang] = nat_name
            
        else:
            nat_name = nat_names_row.find_element(By.XPATH, ".//span[1]").text
            lang_text = nat_names_row.find_element(By.XPATH, ".//span[@class='languageicon']").text
            nat_lang = lang_text.replace('(', '').replace(')', '').lower()
            native_names[nat_lang] = nat_name

        driver.back()
        # just to slow down, on my laptop it cant load shit fast
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
        )
        sleep(1)
        
    except:
        native_names["english"] = common_name
    
    flag_img = ''
    try:
        flag_img_prop = main.find_element(By.ID, prop['flag_img'])
        flag_img_row = flag_img_prop.find_element(By.CLASS_NAME, "listview-item")
        flag_img_item = flag_img_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
        flag_page_url = flag_img_item.find_element(By.XPATH, './/a').get_attribute('href')
        
        driver.get(flag_page_url)
        flag_body_page = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
        )
        sleep(1)
        flag_img_div = flag_body_page.find_element(By.ID, 'file')
        flag_img = flag_img_div.find_element(By.XPATH, './/a').get_attribute('href')
        driver.back()
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, ""))
        )
        pass
    except:
        pass
    
    capital_name = ''
    capital_nn = []
    # capital_nn = {}
    # capital_loc = ''
    capital_pop = '0'
    capital_flag = ''
    try:
        sleep(1)
        cap_prop = main.find_element(By.ID, prop['capital'])
        try:
            cap_row = cap_prop.find_element(By.CLASS_NAME, "wb-preferred")
        except:
            cap_row = cap_prop.find_element(By.CLASS_NAME, "listview-item")

        cap_item = cap_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
        capital_name = cap_item.text
        wdata_cap_url = cap_item.find_element(By.XPATH, './/a').get_attribute('href')
        
        driver.get(wdata_cap_url)
        wdata_cap_page = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
        )
        try:
            sleep(1)
            cap_nn_prop = wdata_cap_page.find_element(By.ID, prop['native_label'])
            cap_nn_rows = cap_nn_prop.find_elements(By.CLASS_NAME, "listview-item")
            for cap_nn_row in cap_nn_rows:
                cap_nn_item = cap_nn_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
                cap_nn_spans = cap_nn_item.find_elements(By.TAG_NAME, "span")
                cap_nn_text = cap_nn_spans[0].text
                capital_nn.append(cap_nn_text)
        except:
            capital_nn["english"] = common_name
        try:
            sleep(1)
            cap_pop_prop = wdata_cap_page.find_element(By.ID, prop['population'])
            cap_pop_rows = cap_pop_prop.find_elements(By.CLASS_NAME, "wb-preferred")
            for cap_pop_row in cap_pop_rows:
                capital_pop = cap_pop_row.find_element(By.CLASS_NAME, "wikibase-snakview-value").text
        except:
            pass
        
        if wdata_cap_page.find_element(By.ID, prop['flag_img']):
            sleep(1)
            cap_flag_prop = wdata_cap_page.find_element(By.ID, prop['flag_img'])
            cap_flag_row = cap_flag_prop.find_element(By.CLASS_NAME, "listview-item")
            cap_flag_item = cap_flag_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
            cap_flag_page_url = cap_flag_item.find_element(By.XPATH, './/a').get_attribute('href')
            
            driver.get(cap_flag_page_url)
            flag_body_page = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
            )
            sleep(1)
            cap_flag_div = flag_body_page.find_element(By.ID, 'file')
            capital_flag = cap_flag_div.find_element(By.XPATH, './/a').get_attribute('href')
        elif not wdata_cap_page.find_element(By.ID, prop['flag_img']):
            sleep(1)
            wpedia_cap_url = f'https://en.wikipedia.org/wiki/{capital_name}'
            driver.get(wpedia_cap_url)
            wpedia_cap_page = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME, "infobox"))
            )
            sleep(1)
            
            try:
                cap_flag_row = wpedia_cap_page.find_element(By.CLASS_NAME, "maptable")
                cap_flag_items = cap_flag_row.find_elements(By.CLASS_NAME, "ib-settlement-cols-cell")
                
                for cap_flag_item in cap_flag_items:
                    cap_flag_label = cap_flag_item.find_element(By.CLASS_NAME, "ib-settlement-caption-link").text

                    if 'Flag' in cap_flag_label:
                        cap_flag_page_url = cap_flag_item.find_element(By.XPATH, './/span/a').get_attribute('href')
                        driver.get(cap_flag_page_url)
                        cap_flag_page = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
                        )
                        sleep(1)
                        cap_flag_div = cap_flag_page.find_element(By.ID, 'file')
                        capital_flag = cap_flag_div.find_element(By.XPATH, './/a').get_attribute('href')
            except:
                pass
    except:
        pass

    data.append({
        
        "name": {
            "common": common_name,
            "official": official_name,
            "native": native_names
        },
        
        "population": population,
        
        "flag": flag_img,
        "demonym": demonyms,
        
        "capital": {
            "name": {
                "common": capital_name,
                "native": capital_nn
            },
            "population": capital_pop,
            "flag": capital_flag
        },
        # "cities": [] # in later versions
        
        "area": {
            "total": total_area,
            "land": total_land_area,
            "water%": water_perc
        },
        "continents": continents,
        "part of": a_part_of,
        
        "iso-code": {
            "alpha-2": alpha_2_code,
            "alpha-3": alpha_3_code,
            "numeric": numeric_code,
            "iso-2": subdiv_code # kinda more specific when comes to territories/not independent countries
        },

        # "languages": {
        #     "official": official_langs,
        #     "spoken": spoken_langs
        # },
        # test look v^
        "official_lang": official_langs,
        
        # "religions": religions,
        # "ethnicities": ethnicities,
        
        # ("religions" if religions > 1 else "religion"): religions
        
    })
    save_to_json(data, json_file_path)
    
data = []

for place_url in imp_data['place']:
    process_url(place_url, data)

driver.quit()
