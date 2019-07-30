"""Graphing notebook for publication frequency as compared to BTC price / volatility."""

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

bbc_per_day = bbc.groupby([pd.Grouper(key='published', freq='D')])['content'].count()
bbc_per_day = bbc_per_day.reindex(data.raw_index_days)
bbc_per_day[np.isnan(bbc_per_day)] = 0

bbc_per_month = bbc_per_day.rolling(30).mean()
bbc_per_month[np.isnan(bbc_per_month)] = 0

bbc_per_fn = bbc_per_day.rolling(14).mean()
bbc_per_fn[np.isnan(bbc_per_fn)] = 0

cnn_per_day = cnn.groupby([pd.Grouper(key='published', freq='D')])['content'].count()
cnn_per_day = cnn_per_day.reindex(data.raw_index_days)
cnn_per_day[np.isnan(cnn_per_day)] = 0

cnn_per_month = cnn_per_day.rolling(30).mean()
cnn_per_month[np.isnan(cnn_per_month)] = 0
cnn_per_fn = cnn_per_day.rolling(14).mean()
cnn_per_fn[np.isnan(cnn_per_fn)] = 0

nyt_per_day = nyt.groupby([pd.Grouper(key='published', freq='D')])['content'].count()
nyt_per_day = nyt_per_day.reindex(data.raw_index_days)
nyt_per_day[np.isnan(nyt_per_day)] = 0

nyt_per_month = nyt_per_day.rolling(30).mean()
nyt_per_month[np.isnan(nyt_per_month)] = 0
nyt_per_fn = nyt_per_day.rolling(14).mean()
nyt_per_fn[np.isnan(nyt_per_fn)] = 0

reuters_per_day = reuters.groupby([pd.Grouper(key='published', freq='D')])['content'].count()
reuters_per_day = reuters_per_day.reindex(data.raw_index_days)
reuters_per_day[np.isnan(reuters_per_day)] = 0

reuters_per_month = reuters_per_day.rolling(30).mean()
reuters_per_month[np.isnan(reuters_per_month)] = 0
reuters_per_fn = reuters_per_day.rolling(14).mean()
reuters_per_fn[np.isnan(reuters_per_fn)] = 0

agg_per_fn = bbc_per_fn + cnn_per_fn + nyt_per_fn + reuters_per_fn
agg_per_month = bbc_per_month + cnn_per_month + nyt_per_month + reuters_per_month

def plotter(data_in_fn, data_in_month, file_key):
    """Plotting function parent for publish quantity vs. BTC price."""

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16, 4)
    ax.set_xlim(data.start_point.date(), data.end_point.date())

    line1 = ax.plot(data_in_month, label='Monthly')
    line2 = ax.plot(data_in_fn, label='Fortnightly')

    ax2 = ax.twinx()
    line3 = ax2.plot(btc, label='BTC', c = 'red', alpha = 0.7)

    lines = line1 + line2 + line3
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, handlelength=2, loc=0)
    plt.savefig(f'plots/btc_publish_count_rolling/rolling_publish_btc_{file_key}.png', dpi=150, transparent=True)

### Run plotting functions ###
plotter(bbc_per_fn, bbc_per_month, 'bbc')
plotter(cnn_per_fn, cnn_per_month, 'cnn')
plotter(nyt_per_fn, nyt_per_month, 'nyt')
plotter(reuters_per_fn, reuters_per_month, 'reuters')
plotter(agg_per_fn, agg_per_month, 'agg')
