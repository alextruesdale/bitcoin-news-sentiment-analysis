"""Module containing VADER analysis / scoring of scraped news text data."""

import sentiment_base as base
import pandas as pd
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

class SentimentScorer(object):
    """"""

    def __init__(self):

        nltk.download('vader_lexicon')
        self.sentiment = SentimentIntensityAnalyzer()

        self.bbc_frame = base.file_reader('bbc')
        self.cnn_frame = base.file_reader('cnn')
        self.nyt_frame = base.file_reader('nyt')
        self.reuters_frame = base.file_reader('reuters')

    def sentiment_scorer(self, stories_sentences):
        """
        VADER and TextBlob scoring function; splits stories by sentence,
        takes respective sentence sentiment, averages sentences for overall story sentiment.
        """

        vader_scores = [np.mean([score['compound'] for score in [self.sentiment.polarity_scores(sentence) for sentence in story]]) for story in stories_sentences]
        textblob_scores = [np.mean([TextBlob(sentence).sentiment.polarity for sentence in story]) for story in stories_sentences]
        return vader_scores, textblob_scores

    def scorer_handler(self, frame, name):
        """Handler for vader scoring method accross source files."""

        frame = base.story_filter(frame)

        stories = list(frame['content'])
        stories_sentences = [story.split('. ') for story in stories]

        frame['vader_score'], frame['textblob_score'] = self.sentiment_scorer(stories_sentences)
        print(frame.head(5))
        return frame

    def save_frames(self):
        """Save scored dataframes to appropriate data directory."""

        self.bbc_frame.to_csv(f'../data/scored/bbc_bitcoin_scored.csv')
        self.cnn_frame.to_csv(f'../data/scored/cnn_bitcoin_scored.csv')
        self.nyt_frame.to_csv(f'../data/scored/nyt_bitcoin_scored.csv')
        self.reuters_frame.to_csv(f'../data/scored/reuters_bitcoin_scored.csv')
