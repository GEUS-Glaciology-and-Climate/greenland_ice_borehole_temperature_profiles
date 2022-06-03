#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
import os
import seaborn as sns
import glob

m_dirs = glob.glob('boreholes/*')

bhs = []
for m_dir in m_dirs:
    d_file = os.path.join(m_dir, "data.csv")
    m_file = os.path.join(m_dir, "meta.bsv")

    if os.path.isfile(d_file):
        d = pd.read_csv(d_file).rename(columns={"t": "Temperature [Celsius]", "d": "Depth [m]"})
        m = pd.read_csv(m_file, sep="|", index_col=0).T
        d["Borehole ID"] = [m.index.values[0]] * len(d)
        dm = pd.merge(d, m.reset_index(), left_on="Borehole ID", right_on="index").drop(columns=["index"])
        bhs.append(dm)
df = pd.concat(bhs).reset_index()
df.to_csv("data/merged_data.csv.gz")

# Plot each borehole.
for bh in df["Borehole ID"].unique():
    g = sns.lineplot(data=df[df["Borehole ID"] == bh], x="Temperature [Celsius]", y="Depth [m]")
    g.axes.invert_yaxis()
