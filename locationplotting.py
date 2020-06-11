import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



# Extract the data we're interested in
lat = cities['Latitude'].values
lon = cities['Longitude'].values

# 1. Draw the map background
fig = plt.figure(figsize=(10, 10))
m = Basemap(resolution='c',projection='merc',lat_0=54.5,lon_0=-4.36,llcrnrlon=-6.,llcrnrlat= 49.5,urcrnrlon=2.,urcrnrlat=55.2)
m.drawmapboundary(fill_color='#46bcec')

m.drawcoastlines()


# 2. scatter city data, with color reflecting population
# and size reflecting area
m.scatter(lon, lat, latlon=True,cmap='Reds', alpha=0.3)
###############################################################################
import gmplot
from gmplot import *
import pandas as pd
df = pd.read_excel('LocupdatedData.xlsx')

lat = df['Latitude'].values
lon = df['Longitude'].values


#gmap.scatter(lat,lon, c='r',size=100, marker=True)
gmap=gmplot.GoogleMapPlotter(54.02,-0.94,6.5)
gmap.apikey = "AIzaSyAhzINZ3b25CuR5ldJOdouaQLRE8_lUD78"

gmap.heatmap(lat,lon,radius=15,dissipating=True)
gmap.draw( "maps.html" )

###############################################################################




import gmaps
import pandas as pd
from ipywidgets.embed import embed_minimal_html

df = pd.read_excel('LocupdatedData.xlsx')

gmaps.configure(api_key='AIzaSyAhzINZ3b25CuR5ldJOdouaQLRE8_lUD78')
ukco = (54.02,-0.94)
gmaps.figure(center=ukco, zoom_level=6)
locations = df[['Latitude', 'Longitude']]
fig = gmaps.figure()

fig.add_layer(gmaps.heatmap_layer(locations))
embed_minimal_html('export.html', views=[fig])
