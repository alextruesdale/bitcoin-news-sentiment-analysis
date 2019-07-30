"""Graphing notebook for TextBlob sentiment against BTC price / volatility."""

import sys
sys.path.append('analysis')
from analysis_base import AnalysisBase

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = AnalysisBase()
bbc = data.bbc
cnn = data.cnn
nyt = data.nyt
reuters = data.reuters
btc = data.btc

bbc_per_day = bbc.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
bbc_per_day = bbc_per_day.reindex(data.raw_index_days)

cnn_per_day = cnn.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
cnn_per_day = cnn_per_day.reindex(data.raw_index_days)

nyt_per_day = nyt.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
nyt_per_day = nyt_per_day.reindex(data.raw_index_days)

reuters_per_day = reuters.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
reuters_per_day = reuters_per_day.reindex(data.raw_index_days)

agg_per_day = bbc_per_day.to_frame().join(cnn_per_day, lsuffix='_left').join(nyt_per_day, lsuffix='_left').join(reuters_per_day, lsuffix='_left')
agg_per_day = np.nanmean(agg_per_day, axis=1)
agg_per_day = pd.Series(agg_per_day)
agg_per_day.index = data.raw_index_days

bbc_per_day[np.isnan(bbc_per_day)] = 0
cnn_per_day[np.isnan(cnn_per_day)] = 0
nyt_per_day[np.isnan(nyt_per_day)] = 0
reuters_per_day[np.isnan(reuters_per_day)] = 0
agg_per_day[np.isnan(agg_per_day)] = 0

def plotter(data_in, file_key):
    """Plotting function parent for TextBlob sentiment vs. BTC price."""

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16, 4)
    ax.set_xlim(data.start_point.date(), data.end_point.date())

    line1 = ax.plot(data_in.rolling(30).mean(),label='Monthly')
    line2 = ax.plot(data_in.rolling(14).mean(),label='Fortnightly')

    ax2 = ax.twinx()
    line3 = ax2.plot(btc, label='BTC', c = 'red', alpha = 0.7)

    lines = line1 + line2 + line3
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, handlelength=2, loc=0)
    plt.savefig(f'plots/btc_textblob_sentiment/rolling_blob_btc_{file_key}.png', dpi=150, transparent=True)

### Run plotting functions ###
plotter(bbc_per_day, 'bbc')
plotter(cnn_per_day, 'cnn')
plotter(nyt_per_day, 'nyt')
plotter(reuters_per_day, 'reuters')
plotter(agg_per_day, 'agg')
