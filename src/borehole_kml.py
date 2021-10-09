import pandas as pd
import simplekml
import cgi
import numpy as np

df = pd.read_csv('./data/meta.csv', index_col=0)

kml = simplekml.Kml()
for site in df.index:
    coords=df.loc[site]['Longitude [°E]'], df.loc[site]['Latitude [°N]']
    if np.all(np.isfinite(coords)):
        p = kml.newpoint(name=site, coords=[coords])
        for n in df.loc[site].index:
            p.extendeddata.newdata(n, cgi.html.escape(str(df.loc[site, n])))
                                    
kml.save('./data/boreholes.kml')
