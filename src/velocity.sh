
grass -e -c EPSG:3413 G
grass ./G/PERMANENT

v.import input=boreholes.kml output=boreholes

r.in.gdal input="NetCDF:/home/kdm/data/ITS_LIVE/CAN_G0120_0000.nc:v" output=v_can
r.in.gdal input="NetCDF:/home/kdm/data/ITS_LIVE/GRE_G0120_0000.nc:v" output=v_gre

g.region raster=v_can,v_gre -pa
r.patch input=v_can,v_gre output=v

d.mon wx0
d.rast v
d.vect boreholes color=red width=3

v.what.rast map=boreholes type=point raster=v column=v
db.select sql="select Name,v from boreholes" # Check order is correct
db.select sql="select v from boreholes" # Paste into DB?
