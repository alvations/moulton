
import sys
import warnings
import time

from tqdm import tqdm
from bs4 import BeautifulSoup
import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from moulton.utils import open_chrome

def get_gscholar(gscholar_url, output_json_filename):
    driver = open_chrome(False)
    driver.get(gscholar_url)

    # Scroll down to list all articles.
    while True:
        e = driver.find_element_by_xpath('//button[@id="gsc_bpf_more"]')
        e.click()
        if e.get_attribute('disabled') == 'true':
            break
    time.sleep(0.7)
    
    # Collect all publications listed.
    publications = []

    for e in tqdm(driver.find_elements_by_xpath('//tr[@class="gsc_a_tr"]')):
        # Clicking on individual article.
        WebDriverWait(e, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//a[(@class="gsc_a_at") and contains(text(), "{}")]'.format(
                    e.text.split('\n')[0])))).click()
        _json = {}
        time.sleep(0.7)
        print(e.text)
        bsoup = BeautifulSoup(driver.page_source.encode('utf-8'))
        cite = bsoup.find('div', attrs={'id': 'gs_md_cita-l'})
        keys = cite.find_all('div', attrs={'class':'gsc_vcd_field'})
        values = cite.find_all('div', attrs={'class':'gsc_vcd_value'})
        for k,v in zip(keys, values):
            if k.text == 'Scholar articles':
                continue
            if k.text == 'Total citations':
                _json[k.text] = int(v.find('a').text[9:])
            else:
                _json[k.text] = v.get_text('\n')
        print(_json)
        time.sleep(0.7)
        driver.find_element_by_xpath('//a[@id="gs_md_cita-d-x"]').click()

        # Only if the _json is valid and unique, save it.
        if _json:
            json_str = json.dumps(_json)
            if json_str not in publications:
                publications.append(json_str)
        print('#######')
    # Clean up and convert the json string back to a proper json object.
    publications = [json.loads(c) for c in publications]

    # Save the publications in json file.
    with open(output_json_filename, 'w') as fout:
        json.dump(publications, fout)

    return publications
