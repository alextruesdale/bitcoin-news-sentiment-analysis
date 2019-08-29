"""Graphing notebook comparing BTC and Crix price movement over time."""

from analysis_base import AnalysisBase
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = AnalysisBase()
btc = data.btc
crix = data.crix

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(16, 4)
ax.set_xlim(data.start_point.date(), data.end_point.date())
ax2 = ax.twinx()

line1 = ax.plot(btc, c = 'blue')
line2 = ax2.plot(crix, c = 'red', alpha = 0.7)

ax.set_ylabel('Crix Value', color='b', labelpad=10)
ax2.set_ylabel('BTC Price', color='r', labelpad=10)
plt.savefig(f'plots/btc_crix_surrogate.png', dpi=150, transparent=True)
