
import sys
import warnings
import time
from collections import defaultdict

from tqdm import tqdm
from bs4 import BeautifulSoup

import json
import requests
from pprint import pprint

from moulton.utils import open_chrome

def get_semscholar(semscholar_url, output_json_filename):
    driver = open_chrome(True)
    driver.get(semscholar_url)

    # Go through all the pages to get the paper links.
    pages = []
    try:
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            page = driver.find_element_by_xpath('//a[@data-selenium-selector="next-page"]')
            page.click()
            bsoup = BeautifulSoup(driver.page_source)
            pages.append(bsoup)
            time.sleep(1)
    except:
        pass

    # Extract the URLs for all listed publications.
    papers_urls = ['https://www.semanticscholar.org' + article.find('a').attrs['href']
                  for p in pages
                  for article in p.find_all('article', attrs={'class':'search-result'})]

    # Iterate through all publication links to get the necessary data.
    publications = []

    for url in tqdm(papers_urls):
        article = requests.get(url).content.decode('utf8')
        bsoup = BeautifulSoup(article)

        try:
            num_cite = int(bsoup.find('div', attrs={'class':'scorecard_stat__body'}).find('span').text.split(' ')[0])
        except:
            num_cite = 0
        bsoup = BeautifulSoup(article)

        _json = defaultdict(list)
        for meta in bsoup.find_all('meta'):
            try:
                k = meta.attrs['name']
                v = meta.attrs['content']
                _json[k].append(v)
            except:
                continue
        _json['num_cite'] = num_cite
        _json['url'] = url

        json_str = json.dumps(_json)
        if json_str not in publications:
            publications.append(json_str)

    # Clean up the json object.
    publications = [json.loads(c) for c in publications]

    with open(output_json_filename, 'w') as fout:
        json.dump(publications, fout)

    return publications
