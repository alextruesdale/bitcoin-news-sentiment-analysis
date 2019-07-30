"""Plotting notebook for publication frequency per month."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(rc = {'figure.figsize': (11.7, 8.27)})
data = AnalysisBase()
bbc = data.bbc
cnn = data.cnn
nyt = data.nyt
reuters = data.reuters

bbc_per_month = bbc.groupby([pd.Grouper(key='published', freq='M')])['content'].count()
bbc_per_month = bbc_per_month.reindex(data.raw_index_months)
bbc_per_month[np.isnan(bbc_per_month)] = 0

cnn_per_month = cnn.groupby([pd.Grouper(key='published', freq='M')])['content'].count()
cnn_per_month = cnn_per_month.reindex(data.raw_index_months)
cnn_per_month[np.isnan(cnn_per_month)] = 0

nyt_per_month = nyt.groupby([pd.Grouper(key='published', freq='M')])['content'].count()
nyt_per_month = nyt_per_month.reindex(data.raw_index_months)
nyt_per_month[np.isnan(nyt_per_month)] = 0

reuters_per_month = reuters.groupby([pd.Grouper(key='published', freq='M')])['content'].count()
reuters_per_month = reuters_per_month.reindex(data.raw_index_months)
reuters_per_month[np.isnan(reuters_per_month)] = 0

agg_per_month = bbc_per_month + cnn_per_month + nyt_per_month + reuters_per_month

def plotter(data_in, file_key):
    """Plotting function parent for monthly publish quantity bar charts."""

    fig, ax = plt.subplots()
    sns.countplot(data_in, palette=sns.color_palette('Blues_d', n_colors=1))
    ax.set(xlabel='stories published per month', ylabel='count')
    plt.savefig(f'plots/publish_count/publish_count_month_{file_key}.png', transparent = True)

### Run plotting functions ###
plotter(bbc_per_month, 'bbc')
plotter(cnn_per_month, 'cnn')
plotter(nyt_per_month, 'nyt')
plotter(reuters_per_month, 'reuters')
plotter(agg_per_month, 'agg')
