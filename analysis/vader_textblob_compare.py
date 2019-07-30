"""Graphing notebook for VADER sentiment against TextBlob sentiment."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = AnalysisBase()
bbc = data.bbc
cnn = data.cnn
nyt = data.nyt
reuters = data.reuters

bbc_per_day = pd.DataFrame()
bbc_per_day['vader'] = bbc.groupby([pd.Grouper(key='published', freq='D')])['vader_score'].mean()
bbc_per_day['blob'] = bbc.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
bbc_per_day = bbc_per_day.reindex(data.raw_index_days)
bbc_per_day[np.isnan(bbc_per_day)] = 0

bbc_per_fn_vader = bbc_per_day['vader'].rolling(14).mean()
bbc_per_fn_blob = bbc_per_day['blob'].rolling(14).mean()

cnn_per_day = pd.DataFrame()
cnn_per_day['vader'] = cnn.groupby([pd.Grouper(key='published', freq='D')])['vader_score'].mean()
cnn_per_day['blob'] = cnn.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
cnn_per_day = cnn_per_day.reindex(data.raw_index_days)
cnn_per_day[np.isnan(cnn_per_day)] = 0

cnn_per_fn_vader = cnn_per_day['vader'].rolling(14).mean()
cnn_per_fn_blob = cnn_per_day['blob'].rolling(14).mean()

nyt_per_day = pd.DataFrame()
nyt_per_day['vader'] = nyt.groupby([pd.Grouper(key='published', freq='D')])['vader_score'].mean()
nyt_per_day['blob'] = nyt.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
nyt_per_day = nyt_per_day.reindex(data.raw_index_days)
nyt_per_day[np.isnan(nyt_per_day)] = 0

nyt_per_fn_vader = nyt_per_day['vader'].rolling(14).mean()
nyt_per_fn_blob = nyt_per_day['blob'].rolling(14).mean()

reuters_per_day = pd.DataFrame()
reuters_per_day['vader'] = reuters.groupby([pd.Grouper(key='published', freq='D')])['vader_score'].mean()
reuters_per_day['blob'] = reuters.groupby([pd.Grouper(key='published', freq='D')])['textblob_score'].mean()
reuters_per_day = reuters_per_day.reindex(data.raw_index_days)
reuters_per_day[np.isnan(reuters_per_day)] = 0

reuters_per_fn_vader = reuters_per_day['vader'].rolling(14).mean()
reuters_per_fn_blob = reuters_per_day['blob'].rolling(14).mean()

agg_per_fn_vader = bbc_per_fn_vader.to_frame().join(cnn_per_fn_vader, lsuffix='_left').join(nyt_per_fn_vader, lsuffix='_left').join(reuters_per_fn_vader, lsuffix='_left')
agg_per_fn_vader = np.nanmean(agg_per_fn_vader, axis=1)
agg_per_fn_vader = pd.Series(agg_per_fn_vader)
agg_per_fn_vader.index = data.raw_index_days
agg_per_fn_vader[np.isnan(agg_per_fn_vader)] = 0

agg_per_fn_blob = bbc_per_fn_blob.to_frame().join(cnn_per_fn_blob, lsuffix='_left').join(nyt_per_fn_blob, lsuffix='_left').join(reuters_per_fn_blob, lsuffix='_left')
agg_per_fn_blob = np.nanmean(agg_per_fn_blob, axis=1)
agg_per_fn_blob = pd.Series(agg_per_fn_blob)
agg_per_fn_blob.index = data.raw_index_days
agg_per_fn_blob[np.isnan(agg_per_fn_blob)] = 0

def plotter(data_in_vader, data_in_blob, file_key):
    """Plotting function parent for VADER sentiment vs. BTC price."""

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16, 4)
    ax.set_xlim(data.start_point.date(), data.end_point.date())

    line1 = ax.plot(data_in_vader, label='VADER')
    line2 = ax.plot(data_in_blob, label='TextBlob')

    lines = line1 + line2
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, handlelength=2, loc=0)
    plt.savefig(f'plots/vader_blob_compare/vader_blob_{file_key}.png', dpi=150, transparent=True)

### Run plotting functions ###
plotter(bbc_per_fn_vader, bbc_per_fn_blob, 'bbc')
plotter(cnn_per_fn_vader, cnn_per_fn_blob, 'cnn')
plotter(nyt_per_fn_vader, nyt_per_fn_blob, 'nyt')
plotter(reuters_per_fn_vader, reuters_per_fn_blob, 'reuters')
plotter(agg_per_fn_vader, agg_per_fn_blob, 'agg')
