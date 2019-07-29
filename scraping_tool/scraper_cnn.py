"""Module containing CNN site-specific scraping methods."""

from bs4 import BeautifulSoup
from scraper_base import ScraperBase, Actions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pprint import pprint

import pandas as pd
import time
import re

class CNNScraper:
    """Selenium connection to CNN search page with bound methods."""

    def __init__(self):

        self.base = ScraperBase(fresh=True)
        self.driver = self.base.driver
        self.query_terms = self.base.query_terms

    def query_cnn(self):
        """Capture URL addresses for search results."""

        query_base = 'https://edition.cnn.com/search/?q={}{}{}&type=article'
        query_string = query_base.format(*self.query_terms)
        self.driver.get(query_string)
        self.driver.implicitly_wait(20)

        total_item_string = self.driver.find_element_by_class_name('cnn-search__results-count').text
        total_item_count = int(re.search('.*out\sof\s(\d+).*', total_item_string).group(1))
        search_range = [str(value) for value in list(range(0, total_item_count, 30))]

        elements_extracted_all = {}
        for grouping in search_range:
            query_terms_copy = self.query_terms[:]
            query_terms_copy.append(grouping)

            query_flex = 'https://edition.cnn.com/search/?size=30&q={}{}{}&type=article&from={}'
            query_string = query_flex.format(*query_terms_copy)

            self.driver.get(query_string)
            full_page_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'cnn-search__result--article')))
            raw_html = BeautifulSoup(self.driver.page_source, features='lxml')
            elements_extracted_all.update(self.story_extractor(raw_html, int(grouping)))

        print(f'Keyword search results: {len(elements_extracted_all)}')
        return elements_extracted_all

    def story_extractor(self, raw_html, base):
        """Extract dictionary of articles and publication dates."""

        stories = raw_html.find_all('div', {'class': 'cnn-search__result--article'})
        published_dates = [article.findChild('span', {'class': 'icon--timestamp'}).findNext('span').get_text() for article in stories]
        headlines = [article.findChild('h3', {'class': 'cnn-search__result-headline'}).get_text().strip().strip('\n') for article in stories]
        hyperlinks = [article.findChild('h3', {'class': 'cnn-search__result-headline'}).findChild('a', recursive=True)['href'].lstrip('//') for article in stories]
        hyperlinks = ['http://' + link if link[:3] == 'www' else link for link in hyperlinks]
        query = [self.query_terms for i in range(0, len(headlines))]
        source = ['reuters' for i in range(0, len(headlines))]
        index = list(range(base, base + 30))

        elements_extracted = {a[0]: [a[4], a[5], a[3], a[2], a[1]] for a in list(zip(index, source, query, published_dates, headlines, hyperlinks))}
        return elements_extracted

    def content_fetcher(self, elements_extracted):
        """Navigate to hyperlink and fetch article text."""

        def nav_scrape(row, iteration):
            """DataFrame wrapper for inserting scraped text into appropriate column."""

            print(f'Scraping source #{row.name}', end='\r')
            hyperlink = row['hyperlink']
            self.driver.get(hyperlink)
            time.sleep(1.2)

            raw_html = BeautifulSoup(self.driver.page_source, features='lxml')
            if raw_html.find('section', {'class': 'zn-body-text'}):
                story = raw_html.find('section', {'class': 'zn-body-text'})
                text = ' '.join([div.get_text() for div in story.find_all(class_='zn-body__paragraph')])
                return text

            elif raw_html.find('div', {'id': 'storytext'}):
                story = raw_html.find('div', {'id': 'storytext'})
                text = ' '.join([p.get_text() for p in story.find_all('p')])

                return text

        content_dataframe = pd.DataFrame.from_dict(elements_extracted, orient='index', columns = ['headline', 'hyperlink', 'published', 'query', 'source'])
        content_dataframe['content'] = content_dataframe.apply(nav_scrape, iteration=1, axis=1)

        return content_dataframe
