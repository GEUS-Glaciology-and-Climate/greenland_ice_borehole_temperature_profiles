import pandas as pd
import numpy as np
import sys

df = pd.read_csv('./data/meta.csv', index_col=0)

for row in df.index:
    bh = df.loc[row]
    bh.index.name = 'Borehole ID'
    try:
        bh.to_csv('./boreholes/' + bh.name + '/meta.bsv', sep='|')
    except:
        assert(False)
