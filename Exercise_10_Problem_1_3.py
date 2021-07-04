#!/usr/bin/env python
# coding: utf-8

# ## Problem 1: Geocode shopping centers
# 
# In problem 1 the task is to find out the addresses for a list of shopping centers and to geocode these addresses in order to represent them as points. The output should be stored in a Shapefile called `shopping_centers.shp` 
# 

# Import modules
import geopandas as gpd
import pandas as pd
# Read the data (replace "None" with your own code)
data = None
# YOUR CODE HERE 1 to read the data
#read the file
#giocodingが上手くいかなかったので住所は丁以降は除外
data=pd.read_csv("data/shopping_centers.txt",delimiter=";")

#TEST COEE
# Check your input data
print(data)

# - Geocode the addresses using the Nominatim geocoding service. Store the output in a variable called `geo`:

# Geocode the addresses using Nominatim
geo = None
from geopandas.tools import geocode

# Geocode addresses using Nominatim. Remember to provide a custom "application name" in the user_agent parameter!
#YOUR CODE HERE 2 for geocoding
#geocoding by using nominatim
geo=geocode(data['addr'],provider='nominatim', user_agent='autogis_xx')
#TEST CODE
# Check the geocoded output
print(geo)

#TEST CODE
# Check the data type (should be a GeoDataFrame!)
print(type(geo))


# Check that the coordinate reference system of the geocoded result is correctly defined, and **reproject the layer into JGD2011** (EPSG:6668):

# YOUR CODE HERE 3 to set crs.
#set crs (epsg=6668)
geo=geo.to_crs(epsg=6668)
#TEST CODE
# Check layer crs
print(geo.crs)


# YOUR CODE HERE 4 to join the tables
#make geodata it contains id,name,geometry,addr
geodata = gpd.GeoDataFrame()
geodata['id']=data['id']
geodata['name']=data['name']
geodata['geometry']=geo['geometry']
geodata['addr']=geo['address']

#TEST CODE
# Check the join output
print(geodata.head())


# - Save the output as a Shapefile called `shopping_centers.shp` 

# Define output filepath
out_fp = 'shopping_centers.shp'
# YOUR CODE HERE 5 to save the output
#save the output
import os
outpath = os.path.join(out_fp)
geodata.to_file(outpath)
# TEST CODE
# Print info about output file
print("Geocoded output is stored in this file:", out_fp)


# ## Problem 2: Create buffers around shopping centers
# 
# Let's continue with our case study and calculate a 1.5 km buffer around the geocoded points. 
 

# YOUR CODE HERE 6 to create a new column
#create new column for calculate buffers
buffer=[]

# YOUR CODE HERE 7 to set buffer column
#set crs
geodata=geodata.to_crs(epsg=32634)
#calculate buffers
buffer=geodata['geometry'].buffer(1500)
#set buffer in geodata['buffer']
geodata['buffer']=buffer

#TEST CODE
print(geodata.head())

#TEST CODE
# Check the data type of the first value in the buffer-column
print(type(geodata.at[0,'buffer']))


#TEST CODE
# Check the areas of your buffers in km^2
print(round(gpd.GeoSeries(geodata["buffer"]).area / 1000000))


# - Replace the values in `geometry` column with the values of `buffer` column:

# YOUR CODE HERE 8 to replace the values in geometry
#replace the value in geometry to buffer 
geodata['geometry']=buffer
#TEST CODE
print(geodata.head())


# ## Problem 3: How many people live near shopping centers? 
# 
# Last step in our analysis is to make a spatial join between our buffer layer and population data in order to find out **how many people live near each shopping center**. 
# 

# YOUR CODE HERE 9
# Read population grid data for 2018 into a variable `pop`. 
pop=gpd.read_file("data/500m_mesh_suikei_2018_shape_13/500m_mesh_2018_13.shp")
pop=pop[['PTN_2020','geometry']]
geodata=geodata.to_crs(epsg=4612)
#TEST CODE
# Check your input data
print("Number of rows:", len(pop))
print(pop.head(3))


# In[ ]:


# Create a spatial join between grid layer and buffer layer. 
# YOUR CDOE HERE 10 for spatial join
pop=gpd.sjoin(pop,geodata,how='inner',op='intersects')
grouped=pop.groupby('addr')
for key, group in grouped:
  if key=="道玄坂, 円山町, 渋谷区, 東京都, 150-0044, 日本":
    TDS=len(group)
  if key=="宇田川通り, 宇田川町, 渋谷区, 東京都, 150-0042, 日本":
    SSS=len(group)
  if key=="日本東京神殿, 木下坂, 六本木六丁目, 南麻布五丁目, 麻布, 港区, 東京都, 106-0047, 日本":
    NA=len(group)

# YOUR CODE HERE 11 to report how many people live within 1.5 km distance from each shopping center
print(str(TDS)+" people live within 1.5 km from Tokyo Department Store")
print(str(SSS)+" people live within 1.5 km from Seibu Shibuya Store")
print(str(NA)+" people live within 1.5 km from National Azabu")

# **Reflections:**
#     
# - How challenging did you find problems 1-3 (on scale to 1-5), and why?
# - What was easy?
# - What was difficult?

# YOUR ANSWER HERE
"""
3
It has some challenging part but many of these had been studied yet.

It is difficult to use group object because I have not understood yet.
"""

# Well done!
