import pandas as pd
import numpy as np
import sys

bh_id = sys.argv[1].split('/')[1]
# bh_id = sys.argv[1]

df = pd.read_csv('./data/meta.csv', index_col=0)
row = df.loc[bh_id]

row.index.name = 'Borehole ID'
try:
    row.to_csv('./boreholes/' + row.name + '/meta.bsv', sep='|')
except:
    assert(False)
