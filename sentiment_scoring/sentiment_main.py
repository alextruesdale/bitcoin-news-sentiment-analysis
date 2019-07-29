"""Main module for sentiment analysis notebooks."""

from sentiment_scorer import SentimentScorer

def main():
    """Main function for sentiment scoring tools."""

    scorer = SentimentScorer()

    scorer.bbc_frame = scorer.scorer_handler(scorer.bbc_frame, 'BBC')
    scorer.cnn_frame = scorer.scorer_handler(scorer.cnn_frame, 'CNN')
    scorer.nyt_frame = scorer.scorer_handler(scorer.nyt_frame, 'NYT')
    scorer.reuters_frame = scorer.scorer_handler(scorer.reuters_frame, 'Reuters')

    scorer.save_frames()

if __name__ == '__main__':
    main()
