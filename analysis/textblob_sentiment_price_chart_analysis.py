"""Graphing notebook for TextBlob sentiment against BTC price / volatility."""

from analysis_base import AnalysisBase
from statsmodels.tsa.stattools import grangercausalitytests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = AnalysisBase()
bbc = data.bbc
cnn = data.cnn
nyt = data.nyt
reuters = data.reuters
btc = data.btc

bbc_per_day = bbc.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
bbc_per_day = bbc_per_day.reindex(data.raw_index_days)
bbc_per_day[np.isnan(bbc_per_day)] = 0

bbc_per_month = bbc_per_day.rolling(30).mean()
bbc_per_fn = bbc_per_day.rolling(14).mean()

cnn_per_day = cnn.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
cnn_per_day = cnn_per_day.reindex(data.raw_index_days)
cnn_per_day[np.isnan(cnn_per_day)] = 0

cnn_per_month = cnn_per_day.rolling(30).mean()
cnn_per_fn = cnn_per_day.rolling(14).mean()

nyt_per_day = nyt.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
nyt_per_day = nyt_per_day.reindex(data.raw_index_days)
nyt_per_day[np.isnan(nyt_per_day)] = 0

nyt_per_month = nyt_per_day.rolling(30).mean()
nyt_per_fn = nyt_per_day.rolling(14).mean()

reuters_per_day = reuters.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
reuters_per_day = reuters_per_day.reindex(data.raw_index_days)
reuters_per_day[np.isnan(reuters_per_day)] = 0

reuters_per_month = reuters_per_day.rolling(30).mean()
reuters_per_fn = reuters_per_day.rolling(14).mean()

agg_per_fn = bbc_per_fn.to_frame().join(cnn_per_fn, lsuffix='_left').join(nyt_per_fn, lsuffix='_left').join(reuters_per_fn, lsuffix='_left')
agg_per_fn = np.nanmean(agg_per_fn, axis=1)
agg_per_fn = pd.Series(agg_per_fn)
agg_per_fn.index = data.raw_index_days
agg_per_fn[np.isnan(agg_per_fn)] = 0

agg_per_month = bbc_per_month.to_frame().join(cnn_per_month, lsuffix='_left').join(nyt_per_month, lsuffix='_left').join(reuters_per_month, lsuffix='_left')
agg_per_month = np.nanmean(agg_per_month, axis=1)
agg_per_month = pd.Series(agg_per_month)
agg_per_month.index = data.raw_index_days
agg_per_month[np.isnan(agg_per_month)] = 0

def plotter(data_in_fn, data_in_month, file_key):
    """Plotting function parent for TextBlob sentiment vs. BTC price."""

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16, 4)
    ax.set_xlim(data.start_point.date(), data.end_point.date())
    ax.set_ylim(0, .5)
    ax2 = ax.twinx()

    line1 = ax.plot(data_in_month, c='blue', alpha=0.4)
    line2 = ax.plot(data_in_fn, c='orange', alpha=0.9)
    line3 = ax2.plot(btc, c='red', alpha=0.7)

    ax.set_ylabel('Normalised TextBlob Sentiment', color='b', labelpad=10)
    ax2.set_ylabel('BTC Price', color='r', labelpad=10)
    plt.savefig(f'../plots/btc_textblob_sentiment/rolling_blob_btc_{file_key}.png', dpi=150, transparent=True)

### Run plotting functions ###
plotter(bbc_per_fn, bbc_per_month, 'bbc')
plotter(cnn_per_fn, cnn_per_month, 'cnn')
plotter(nyt_per_fn, nyt_per_month, 'nyt')
plotter(reuters_per_fn, reuters_per_month, 'reuters')
plotter(agg_per_fn, agg_per_month, 'agg')

### Correlation of time series ###

agg_per_fn = agg_per_fn.iloc[1:-1]
agg_per_fn.corr(btc['price'])

### Correlation of time series ###

test_frame_01 = pd.concat([btc['price'], agg_per_fn], axis=1)
grangercausalitytests(test_frame_01, 70, addconst=True, verbose=True)

test_frame_02 = pd.concat([agg_per_fn, btc['price']], axis=1)
grangercausalitytests(test_frame_02, 70, addconst=True, verbose=True)
