import pandas as pd
import numpy as np

url =  "https://docs.google.com/spreadsheets/d/1QNqnjO7Gocl29Y7X693rCRRZI4dTSq0i58YghWeHy2Q/export?format=csv&gid=765194309"

df = pd.read_csv(url)\
       .set_index('Borehole ID')\
       .drop(columns=['Needs?','High Strain','SMB Regime','Basal State'])\
       .replace('\#DIV/0!', np.nan)\
       .replace('\#VALUE!', np.nan)

# df['Velocity [m/yr]'] = df['Velocity [m/yr]'].round(1)

df.to_csv('./data/meta.csv')
