
import pyderman

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def open_chrome(headless=True):
    path = pyderman.install(browser=pyderman.chrome)

    options = Options()
    options.add_argument("--enable-javascript")
    options.headless = headless

    driver = webdriver.Chrome(path, options=options)

    # Sanity checks.
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    return driver
