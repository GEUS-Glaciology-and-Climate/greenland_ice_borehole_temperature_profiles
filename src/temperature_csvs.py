import os
import glob
import pandas as pd
import numpy as np


index = np.arange(4E3)
df = pd.DataFrame(index=index)
df.index.name = 'd'

boreholes = [_.split('/')[2] for _ in glob.glob('./boreholes/*')]
boreholes = sorted(boreholes)

thick = {}

for b in boreholes:
  print("Borehole: ", b)
  m = pd.read_csv('./boreholes/' + b + '/meta.bsv', sep="|", index_col=0).squeeze()

  # save thickness at each borehole to 1) set to -999 or 2) compute normalized depth
  thick[b] = m['Ice thickness [m]']
  
  d = pd.read_csv('./boreholes/' + b + '/data.csv').set_index('d').rename(columns={'t':m.name})
  d.index = np.round(d.index).astype(int)
  d = d.groupby(d.index).mean()
  df = df.merge(d, left_index=True, right_index=True, how='outer')

df.index.name = "depth [m]"
# interpolate w/ PCHIP no overshoot
df = df.interpolate(limit_area='inside', method='pchip')
df.index = df.index.astype(int)
df = df[df.index > 0]


# set below bedrock to -999
for b in df.columns:
  try: 
    th = int(thick[b])
  except:
    continue
  df[b][th:] = -999

maxdepth = df.replace(-999,np.nan).dropna(how='all').index.max()
df = df[df.index <= maxdepth]
df.to_csv('./data/temperature.csv', float_format='%.4f', na_rep='NaN')

# Normalized
index = np.linspace(0,10000,10001)
dfN = pd.DataFrame(index=index)
dfN.index.name = 'd normalized'

for b in df.columns:
    th = pd.Series(pd.to_numeric(thick[b], errors='coerce'))\
           .replace(np.nan,0)\
           .astype(int).values[0]
    profile = pd.DataFrame(df[b][0:th])
    # Maybe do not round, rather, interpolate to 1 % resolution?
    profile['dNorm'] = np.round(profile.index/th*10000)
    profile = profile.groupby('dNorm').mean()
    profile.index.name = 'd normalized'
    dfN = dfN.merge(profile, left_index=True, right_index=True, how='outer')

dfN = dfN.interpolate(limit_area='inside', method='pchip')
dfN = dfN[::100]
dfN.index = dfN.index/10000
dfN.to_csv('./data/temperature_dnorm.csv', float_format='%.4f', na_rep='NaN')
