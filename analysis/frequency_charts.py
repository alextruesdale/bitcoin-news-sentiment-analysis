"""Plotting notebook for publication frequency per month."""

from analysis_base import AnalysisBase
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

    initial_date_end = data.end_point.date()
    padded_date_end = initial_date_end + dateutil.relativedelta.relativedelta(days=25)

    plt.rcParams["axes.edgecolor"] = '0.15'
    plt.rcParams["axes.linewidth"]  = 1
    fig, ax = plt.subplots()
    fig.set_size_inches(11, 8)
    ax.set_xlim(data.start_point.date(), padded_date_end)
    ax.grid(False)

    ax.bar(data_in.index, data_in, width=1, color='#4984AF')
    ax.set_ylabel('Count Articles Published', labelpad=10)
    plt.savefig(f'../plots/publish_count/publish_count_month_{file_key}.png', dpi=150, transparent = True)

### Run plotting functions ###
plotter(bbc_per_month, 'bbc')
plotter(cnn_per_month, 'cnn')
plotter(nyt_per_month, 'nyt')
plotter(reuters_per_month, 'reuters')
plotter(agg_per_month, 'agg')
