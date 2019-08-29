<img src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/btc_logo.png' alt='BTC logo' title='BTC' align='right' height='115' />

# Bitcoin Sentiment in Large Publications

This repository holds code for a sentiment analysis of Bitcoin-related publications in traditional media (large, popular, print-based sources). The codebase consists of two tools: the web-scraping suite and the functional code which applies the sentiment analysis libraries to the corpus.

## Code

#### Scraping Tool

The scraper has a basic terminal-based interactive component through which a user can choose a scraping source and keywords. The available sources are NTY, CNN, BBC & Reuters. This tool performs a keyword search on the source, collects article hyperlinks, and then extracts article text from the specific webpages, respectively.

#### Sentiment Tool

To derive sentiment scores from the scraped text data, two 'out-of-the-box', unsupervised methods are employed: VADER and TextBlob sentiment libraries. These differ from one another somewhat but provide a similar result in applying pre-trained sentiment polarity values for words known to the model within a given article. Both methods have basic functionality for taking context into account (i.e. negation and so forth).

## Data

2053 articles with keyword = ‘bitcoin’

- BBC (318 stories – avg. length 451 words)
- NYT (402 stories – avg. length 1011 words)
- CNN (720 stories – avg. length 379 words)
- Reuters (602 stories – avg. length 544 words) 

Time range from 2011 to May, 2019

- BBC: June, 2011 – May, 2019
- NYT: January, 2012 – May, 2019
- CNN: August, 2012 – May, 2019
- Reuters: April, 2012 – May, 2019

## Output

Each article receives a sentiment polarity score. Articles are then aggregated in rolling time windows (monthly & fortnightly) to create smooth time series, which are plotted against Bitcoin prices. Additionally, visualisations on publishing frequency and comparison plots between VADER and TextBlob scores are also produced.

### Publishing Frequency Over Time

<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/publication_freq.png' alt='publication_frequency' title='publication_frequency' width='880' />

### Sentiment vs. BTC Price

Sentiment scores are calculated using both VADER and TextBlob polarity scoring. For each data source below, the first plot shows the VADER scores, while the second shows those derived via TextBlob. Cursory causality testing using Granger Causality Tests indicated that, amongst these selected sources, BTC price is more a driver of news sentiment than the other way around.

#### Aggregate
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_vader_btc_agg.png' alt='rolling_vader_btc_agg' title='rolling_vader_btc_agg' width='1000' />

<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_blob_btc_agg.png' alt='rolling_blob_btc_agg' title='rolling_blob_btc_agg' width='1000' />

#### BBC
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_vader_btc_bbc.png' alt='rolling_vader_btc_bbc' title='rolling_vader_btc_bbc' width='1000' />

<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_blob_btc_bbc.png' alt='rolling_blob_btc_bbc' title='rolling_blob_btc_bbc' width='1000' />

#### CNN
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_vader_btc_cnn.png' alt='rolling_vader_btc_cnn' title='rolling_vader_btc_cnn' width='1000' />

<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_blob_btc_cnn.png' alt='rolling_blob_btc_cnn' title='rolling_blob_btc_cnn' width='1000' />

#### NYT
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_vader_btc_nyt.png' alt='rolling_vader_btc_nyt' title='rolling_vader_btc_nyt' width='1000' />

<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_blob_btc_nyt.png' alt='rolling_blob_btc_nyt' title='rolling_blob_btc_nyt' width='1000' />

#### Reuters
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_vader_btc_reuters.png' alt='rolling_vader_btc_reuters' title='rolling_vader_btc_reuters' width='1000' />

<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/rolling_blob_btc_reuters.png' alt='rolling_blob_btc_reuters' title='rolling_blob_btc_reuters' width='1000' />

### VADER / TextBlob Comparison

The general comparison to note between the two methods is that TextBlob produces consistently lower values than VADER in its polarity scoring. What is interesting, however, is that this variance between the two methods is not equal from source to source (e.g. Reuters scores from both methods are much more similar than those from other sources). This indicates that a particular style of journalism might react with these unsupervised sentiment scorers with more volatility than others – presumably based on word choice.

#### Aggregate
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/vader_blob_agg.png' alt='vader_blob_agg' title='vader_blob_agg' width='1000' />

#### BBC
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/vader_blob_bbc.png' alt='vader_blob_bbc' title='vader_blob_bbc' width='1000' />

#### CNN
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/vader_blob_cnn.png' alt='vader_blob_cnn' title='vader_blob_cnn' width='1000' />

#### NYT
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/vader_blob_nyt.png' alt='vader_blob_nyt' title='vader_blob_nyt' width='1000' />

#### Reuters
<img align='center' src='https://github.com/alextruesdale/bitcoin-news-sentiment-analysis/blob/master/repository_media/vader_blob_reuters.png' alt='vader_blob_reuters' title='vader_blob_reuters' width='1000' />
