"""Scraper base module containing general scraper infrastructure methods."""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup

import pandas as pd
import time

class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: time.sleep(time_s))
        return self

class ScraperBase:

    def __init__(self, fresh):

        self.driver = self.driver_bootup()
        if fresh:
            self.query_terms = self.user_defined_terms()

    def driver_bootup(self):
        """Selenium driver """

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.minimize_window()
        return driver

    def user_defined_terms(self):
        """Prompt user for search terms."""

        print('Please enter query terms (words – maximum 3) separated each by a space.')
        user_input = input('Enter terms: ')
        query_terms = [value if i == 0 else f'+{value}' for i, value in enumerate(str(user_input).split())]
        if len(query_terms) > 3:
            query_terms = query_terms[:3]
        elif len(query_terms) < 3:
            padded = ['', '', '']
            for i, value in enumerate(query_terms):
                padded[i] = value
            query_terms = padded

        return query_terms
