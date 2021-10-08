#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
import os
import seaborn as sns

m_dirs = [
    "Agassiz77",
    "Agassiz79a",
    "Agassiz79b",
    "Agassiz84",
    "CampCentury",
    "CampIII_78",
    "CampVI_50",
    "Devon72",
    "Devon73",
    "Devon98",
    "DYE-3",
    "FladeIsblink06",
    "FOXX1",
    "FOXX2",
    "GISP2",
    "GRIP",
    "GULL",
    "HansTausen_Dome",
    "HansTausen_Hare",
    "Isua_10",
    "Isua_11",
    "Isua_12",
    "Isua_13",
    "Isua_14",
    "Isunnguata_13km-10",
    "Isunnguata_27km-11A",
    "Isunnguata_27km-11B",
    "Isunnguata_27km-11C",
    "Isunnguata_27km-12A",
    "Isunnguata_27km-12B",
    "Isunnguata_27km-12C",
    "Isunnguata_33km_14N",
    "Isunnguata_33km_14SA",
    "Isunnguata_33km_14SB",
    "Isunnguata_33km_14W",
    "Isunnguata_33km_15CA",
    "Isunnguata_33km_15CB",
    "Isunnguata_33km_15E",
    "Isunnguata_33km_15N",
    "Isunnguata_33km_15S",
    "Isunnguata_46km-11A",
    "Isunnguata_46km-11B",
    "Isunnguata_M1-10",
    "Isunnguata_M2-10B",
    "Jakobshavn89A",
    "Jakobshavn89B",
    "Jakobshavn89C",
    "Jakobshavn95D_I1",
    "Jakobshavn95D_I2",
    "Jakobshavn95D_T3",
    "Jakobshavn95D_T4",
    "Jakobshavn95D_T5",
    "Meighen67",
    "NEEM",
    "NGRIP",
    "Penny96",
    "PrinceWales05",
    "Renland88",
    "SiteII",
    "StationCentrale",
    "Store_R30_BH19c",
    "Store_S30",
    "TD1_88",
    "TD2_88",
    "TD3_88",
    "TD4_91a",
    "TD4_91b",
    "TD5_90",
    "TD5_91",
    "Tuto_D-11",
]

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
df.to_csv("merged_data.csv.gz")

sns.lineplot(data=df, x="Temperature [Celsius]", y="Depth [m]")
