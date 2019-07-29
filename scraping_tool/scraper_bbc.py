"""Module containing BBC site-specific scraping methods."""

from bs4 import BeautifulSoup
from scraper_base import ScraperBase, Actions

import pandas as pd
import time

class BBCScraper:
    """Selenium connection to BBC search page with bound methods."""

    def __init__(self):

        self.base = ScraperBase(fresh=True)
        self.driver = self.base.driver
        self.query_terms = self.base.query_terms

    def query_bbc(self):
        """Capture URL addresses for search results."""

        query_base = 'https://www.bbc.co.uk/search?q={}{}{}&filter=news'
        query_string = query_base.format(*self.query_terms)
        self.driver.get(query_string)
        self.driver.implicitly_wait(15)
        for i in range(0, 50):
            try:
                bbc_more_btn = self.driver.find_elements_by_class_name('more')
                Actions(self.driver).click(bbc_more_btn[0]).wait(.6).perform()
            except:
                pass

        raw_html = BeautifulSoup(self.driver.page_source, features='lxml')
        return raw_html

    def story_extractor(self, raw_html):
        """Extract dictionary of articles and publication dates."""

        published_dates = [article.findChild('time', recursive=True)['datetime'] for article in raw_html.find_all(lambda tag: tag.has_attr('data-result-number'))]
        headlines = [article.findChild('h1', recursive=True).find('a').get_text() for article in raw_html.find_all(lambda tag: tag.has_attr('data-result-number'))]
        hyperlinks = [article.findChild('a', recursive=True)['href'] for article in raw_html.find_all(lambda tag: tag.has_attr('data-result-number'))]
        query = [self.query_terms for i in range(0, len(headlines))]
        source = ['bbc' for i in range(0, len(headlines))]
        index = list(range(0, len(headlines)))

        elements_extracted = {a[0]: [a[4], a[5], a[3], a[2], a[1]] for a in list(zip(index, source, query, published_dates, headlines, hyperlinks))}
        print(f'Keyword search results: {len(elements_extracted)}')
        return elements_extracted

    def content_fetcher(self, elements_extracted):
        """Navigate to hyperlink and fetch article text."""

        def nav_scrape(row, iteration):
            """DataFrame wrapper for inserting scraped text into appropriate column."""

            if (row.name + 1) % 30 == 0:
                self.driver.quit()
                self.driver = ScraperBase(fresh=False).driver

            print(f'Scraping source #{row.name}', end='\r')
            hyperlink = row['hyperlink']
            self.driver.get(hyperlink)
            self.driver.implicitly_wait(1)
            raw_html = BeautifulSoup(self.driver.page_source, features='lxml')

            if raw_html.find('div', {'class': 'story-body__inner'}) or raw_html.find('div', {'property': 'articleBody'}):
                story = raw_html.find('div', {'class': 'story-body__inner'})
                story = raw_html.find('div', {'property': 'articleBody'})
                text = ' '.join([p.get_text() for p in story.find_all('p')])
                return text
            elif raw_html.find('div', {'class': 'synopsis-toggle__long'}):
                story = raw_html.find('div', {'class': 'synopsis-toggle__long'})
                text = ' '.join([p.get_text() for p in story.find_all('p')])
                return text
            elif raw_html.find('div', {'class': 'vxp-media__summary'}):
                story = raw_html.find('div', {'class': 'vxp-media__summary'})
                text = ' '.join([p.get_text() for p in story.find_all('p') if not p.findChild('i')])
                return text
            else:
                if iteration == 1:
                    nav_scrape(row, 2)

        content_dataframe = pd.DataFrame.from_dict(elements_extracted, orient='index', columns = ['headline', 'hyperlink', 'published', 'query', 'source'])
        content_dataframe['content'] = content_dataframe.apply(nav_scrape, iteration=1, axis=1)
        return content_dataframe
