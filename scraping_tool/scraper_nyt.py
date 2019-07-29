"""Module containing NYT site-specific scraping methods."""

from bs4 import BeautifulSoup
from scraper_base import ScraperBase, Actions

import pandas as pd
import time

class NYTScraper:
    """Selenium connection to NYT search page with bound methods."""

    def __init__(self):

        self.base = ScraperBase(fresh=True)
        self.driver = self.base.driver
        self.query_terms = self.base.query_terms

    def query_nyt(self):
        """Capture URL addresses for search results."""

        query_base = 'https://www.nytimes.com/search?query={}{}{}'
        query_string = query_base.format(*self.query_terms)
        self.driver.get(query_string)
        self.driver.implicitly_wait(20)
        try:
            topic = True
            nyt_topic = self.driver.find_elements_by_class_name('css-107jdae')[0]
            topic_page = nyt_topic.find_element_by_tag_name('a')
            page_url = topic_page.get_attribute('href')
            self.driver.get(page_url)

            btns = self.driver.find_elements_by_tag_name('button')
            nyt_more_btn = [btn for btn in btns if btn.text.lower() == 'show more']
            Actions(self.driver).click(nyt_more_btn[0]).wait(1).perform()

            current_browser_height = self.driver.execute_script('return document.body.scrollHeight')

            while topic:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3.5)

                new_browser_height = self.driver.execute_script('return document.body.scrollHeight')
                if new_browser_height == current_browser_height:
                    break

                current_browser_height = new_browser_height

        except:
            topic = False
            for i in range(0, 80):
                try:
                    btns = self.driver.find_elements_by_tag_name('button')
                    nyt_more_btn = [btn for btn in btns if btn.text.lower() == 'show more']
                    Actions(self.driver).click(nyt_more_btn[0]).wait(1).perform()
                except:
                    pass

        raw_html = BeautifulSoup(self.driver.page_source, features='lxml')
        return (raw_html, topic)

    def story_extractor(self, raw_html, topic):
        """Extract dictionary of articles and publication dates."""

        if topic:
            stories = raw_html.find('div', {'class': 'stream'}).find_all('li')
            stories = [story for story in stories if 'story-id' in story.get('id')]
            published_dates = [article.findChild('time', recursive=True)['datetime'] for article in stories]
            headlines = [article.findChild('h2', recursive=True).get_text().strip().strip('\n') for article in stories]
            hyperlinks = [article.findChild('a', recursive=True)['href'] for article in stories]
            query = [self.query_terms for i in range(0, len(headlines))]
            source = ['nyt' for i in range(0, len(headlines))]
            index = list(range(0, len(headlines)))

        else:
            stories = raw_html.find_all('li', {'class': 'css-1l4w6pd'})
            published_dates = [article.findChild('time', recursive=True).get_text() for article in stories]
            headlines = [article.findChild('h4', recursive=True).get_text().strip().strip('\n') for article in stories]
            hyperlinks = ['https://www.nytimes.com' + article.findChild('a', recursive=True)['href'] for article in stories]
            query = [self.query_terms for i in range(0, len(headlines))]
            source = ['nyt' for i in range(0, len(headlines))]
            index = list(range(0, len(headlines)))

        elements_extracted = {a[0]: [a[4], a[5], a[3], a[2], a[1]] for a in list(zip(index, source, query, published_dates, headlines, hyperlinks))}
        print(f'Keyword search results: {len(elements_extracted)}')
        return elements_extracted

    def content_fetcher(self, elements_extracted):
        """Navigate to hyperlink and fetch article text."""

        def nav_scrape(row):
            """DataFrame wrapper for inserting scraped text into appropriate column."""

            if (row.name + 1) % 3 == 0:
                self.driver.quit()
                self.driver = ScraperBase(fresh=False).driver

            print(f'Scraping Source #{row.name}', end='\r')
            hyperlink = row['hyperlink']
            self.driver.get(hyperlink)
            self.driver.implicitly_wait(1)
            raw_html = BeautifulSoup(self.driver.page_source, features='lxml')

            if raw_html.find('p', {'class': 'story-body-text'}):
                text = ' '.join([p.get_text() for p in raw_html.find_all('p', {'class': 'story-body-text'})])
                return text
            elif raw_html.find('p', {'class': 'css-18icg9x'}):
                text = ' '.join([p.get_text() for p in raw_html.find_all('p', {'class': 'css-18icg9x'})])
                return text

        content_dataframe = pd.DataFrame.from_dict(elements_extracted, orient='index', columns = ['headline', 'hyperlink', 'published', 'query', 'source'])
        content_dataframe['content'] = content_dataframe.apply(nav_scrape, axis=1)
        return content_dataframe
