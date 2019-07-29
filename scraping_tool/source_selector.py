"""Module for source selection and further forking of tasks to sub-modules."""

from scraper_bbc import BBCScraper
from scraper_nyt import NYTScraper
from scraper_reuters import ReutersScraper
from scraper_cnn import CNNScraper

def source_selector(selected_source):
    """Filter function to select correct course of action (scraper method)."""

    if selected_source == 'bbc':
        scraper = BBCScraper()
        terms = '_'.join(term for term in scraper.query_terms if len(term) > 0)
        raw_html = scraper.query_bbc()
        elements_extracted = scraper.story_extractor(raw_html)
        content_dataframe = scraper.content_fetcher(elements_extracted)
        scraper.driver.quit()

    elif selected_source == 'nyt':
        scraper = NYTScraper()
        terms = '_'.join(term for term in scraper.query_terms if len(term) > 0)
        raw_html, topic = scraper.query_nyt()
        elements_extracted = scraper.story_extractor(raw_html, topic)
        content_dataframe = scraper.content_fetcher(elements_extracted)
        scraper.driver.quit()

    elif selected_source == 'reuters':
        scraper = ReutersScraper()
        terms = '_'.join(term for term in scraper.query_terms if len(term) > 0)
        raw_html = scraper.query_reuters()
        elements_extracted = scraper.story_extractor(raw_html)
        content_dataframe = scraper.content_fetcher(elements_extracted)
        scraper.driver.quit()

    elif selected_source == 'cnn':
        scraper = CNNScraper()
        terms = '_'.join(term for term in scraper.query_terms if len(term) > 0)
        elements_extracted = scraper.query_cnn()
        content_dataframe = scraper.content_fetcher(elements_extracted)
        scraper.driver.quit()

    content_dataframe = content_dataframe.loc[~content_dataframe['content'].isnull()]
    return content_dataframe, terms
