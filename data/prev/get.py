from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def get_country_data(driver):
    try:
        main = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mw-body"))
        )
        
        # names
        common_name = main.find_element(By.CLASS_NAME, "wikibase-title-label").text
        
        en_lang = '(English)'
        
        try:
            prop_1448 = main.find_element(By.ID, "P1448")
            on_rows = prop_1448.find_elements(By.CLASS_NAME, "wikibase-statementview")
            for on_row in on_rows:
                on_item = on_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
                on_spans = on_item.find_elements(By.TAG_NAME, "span")
                if len(on_spans) > 1:
                    if en_lang in on_spans[1].text:
                        official_name = on_spans[0].text
                        print(official_name)
                        return official_name
                    else:
                        print("no span with en_lang")
                else:
                    print("no span")
        except:
            official_name = common_name
            print(official_name)
            return official_name
 
        # try:
        #     prop_1705 = main.find_element(By.ID, "P1705")
        #     nn_rows = prop_1705.find_elements(By.CLASS_NAME, "wikibase-statementview")
            
        #     native_names = []
            
        #     for nn_row in nn_rows:
        #         nn_item = nn_row.find_element(By.CLASS_NAME, "wikibase-snakview-value")
        #         nn_span = nn_item.find_element(By.TAG_NAME, "span")
        #         native_names.append(nn_span.text)

        #     return native_names
        # except:
        #     native_names = []
        #     return native_names
            
        
        # flag
        # try:
        #     flag_element = main.find_element(By.XPATH, ".//tr/td/div/div/div/span/a")
        # except:
        #     flag_element = main.find_element(By.XPATH, ".//tr/td/div/div/span/a")
        # flag_element.click()        
        # flag_zoom_e = WebDriverWait(driver, 50).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "mw-mmv-wrapper"))
        # )
        # flag = flag_zoom_e.find_element(By.CLASS_NAME, "mw-mmv-final-image").get_attribute('src')
        
        # native_common, native_official = '',''
        
    except Exception as e:
        print(f"error fetching country name: {e}")
        
    country_data = {
        "common_name": common_name,
        "official_name": official_name
        # "native_names": native_names,
        # "codes": {
            
        # },
        # "population": population,
        # "flag": flag
}
    return country_data