"""Module containing Reuters site-specific scraping methods."""

from bs4 import BeautifulSoup
from scraper_base import ScraperBase, Actions

import pandas as pd
import time

class ReutersScraper:
    """Selenium connection to Reuters search page with bound methods."""

    def __init__(self):

        self.base = ScraperBase(fresh=True)
        self.driver = self.base.driver
        self.query_terms = self.base.query_terms

    def query_reuters(self):
        """Capture URL addresses for search results."""

        query_base = 'https://www.reuters.com/search/news?sortBy=&dateRange=&blob={}{}{}'
        query_string = query_base.format(*self.query_terms)
        self.driver.get(query_string)
        self.driver.implicitly_wait(20)

        self.driver.find_element_by_id('_evidon-accept-button').click()
        for i in range(0, 100):
            try:
                reuters_more_btn = self.driver.find_elements_by_class_name('search-result-more-txt')
                Actions(self.driver).click(reuters_more_btn[0]).wait(.8).perform()
            except:
                pass

        raw_html = BeautifulSoup(self.driver.page_source, features='lxml')
        return raw_html

    def story_extractor(self, raw_html):
        """Extract dictionary of articles and publication dates."""

        stories = raw_html.find_all('div', {'class': 'search-result-indiv'})
        published_dates = [article.findChild('h5', recursive=True).get_text() for article in stories]
        headlines = [article.findChild('h3', recursive=True).findChild('a', recursive=True).get_text() for article in stories]
        hyperlinks = ['https://www.reuters.com' + article.findChild('h3', recursive=True).findChild('a', recursive=True)['href'] for article in stories]
        query = [self.query_terms for i in range(0, len(headlines))]
        source = ['reuters' for i in range(0, len(headlines))]
        index = list(range(0, len(headlines)))

        elements_extracted = {a[0]: [a[4], a[5], a[3], a[2], a[1]] for a in list(zip(index, source, query, published_dates, headlines, hyperlinks))}
        print(f'Keyword search results: {len(elements_extracted)}')
        return elements_extracted

    def content_fetcher(self, elements_extracted):
        """Navigate to hyperlink and fetch article text."""

        def nav_scrape(row, iteration):
            """DataFrame wrapper for inserting scraped text into appropriate column."""

            print(f'Scraping source #{row.name}', end='\r')
            hyperlink = row['hyperlink']
            self.driver.get(hyperlink)
            self.driver.implicitly_wait(1)
            raw_html = BeautifulSoup(self.driver.page_source, features='lxml')

            if raw_html.find('div', {'class': 'StandardArticleBody_body'}):
                story = raw_html.find('div', {'class': 'StandardArticleBody_body'})
                text = ' '.join([p.get_text() for p in story.find_all('p')])

                return text

        content_dataframe = pd.DataFrame.from_dict(elements_extracted, orient='index', columns = ['headline', 'hyperlink', 'published', 'query', 'source'])
        content_dataframe['content'] = content_dataframe.apply(nav_scrape, iteration=1, axis=1)
        return content_dataframe
