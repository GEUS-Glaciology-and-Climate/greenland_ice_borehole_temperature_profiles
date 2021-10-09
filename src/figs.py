import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc
import pandas as pd
import numpy as np

rc('font', size=10)
rc('text', usetex=False)
# matplotlib.pyplot.xkcd()

# plt.close(1)
fig = plt.figure(1, figsize=(4*2,5*2)) # w,h

fig.clf()
fig.set_tight_layout(True)
ax = fig.add_subplot(111)

df = pd.read_csv('./data/temperature.csv', index_col=0)
df = df.replace(-999, np.nan)
for c in df.columns:
    ax.plot(df[c], -df.index, label=c)
    if np.size(df[c].dropna()) != 0:
        ax.text(df[c].dropna().values[-1],
                -df[c].dropna().index[-1],
                c[0])

ax.set_xlabel('T [°C]')
ax.set_ylabel('Depth below surface [m]')
plt.savefig('./data/temperature.png', transparent=False, bbox_inches='tight', dpi=300)



fig.clf()
fig.set_tight_layout(True)
ax = fig.add_subplot(111)

df = pd.read_csv('./data/temperature_dnorm.csv', index_col=0)
df = df.replace(-999, np.nan)
for c in df.columns:
    ax.plot(df[c], df.index, label=c)
    if np.size(df[c].dropna()) != 0:
        ax.text(df[c].dropna().values[0],
                df[c].dropna().index[0],
                c[0])

ax.set_xlabel('T [°C]')
ax.set_ylabel('Normalized depth below surface [-]')
ax.set_ylim([1,0])
plt.savefig('./data/temperature_dnorm.png', transparent=False, bbox_inches='tight', dpi=300)
