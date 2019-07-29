"""Main module for scraping suite."""

from pick import pick
from source_selector import source_selector

def main():
    """Main function for news source data scraping tool."""

    title = 'Please select a news source from which to gather text data (press ENTER to select indicated option): '
    options = ['BBC', 'NYT', 'Reuters', 'CNN']
    selected_source = pick(options, title, multi_select=False, min_selection_count=1)[0].lower()
    source_data, query = source_selector(selected_source)

    source_data.to_csv(f'data/scraped/{selected_source}_{query}.csv')

if __name__ == '__main__':
    main()
