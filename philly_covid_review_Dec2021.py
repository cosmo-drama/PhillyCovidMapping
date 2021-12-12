#imports
from pickle import FALSE
import geopandas
import numpy as np
import pandas as pd
from matplotlib import *
from matplotlib import pyplot as plt
import datetime
from uszipcode import SearchEngine, SimpleZipcode, Zipcode
from geopandas import read_file


#configs to print all rows and column
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

#pull in data
#path = r"/Users/yasminayala/Desktop/Philly Covid/data/covid_cases_by_zip.csv"
path = r"/home/acorn/Projects/PhillyCovidMapping/covid_cases_by_zip.csv"
df = pd.read_csv(path)


#Cleaning: select rows, select positive cases, arrange by count
    #choose columns
main_data = df.iloc[:, 2:6]
    #filter down to positive case counts only 
pos_data = main_data[main_data.covid_status !="NEG"]
    #sort by count
pos_data_count_sort = pos_data.sort_values('count', ascending=False)
    #fix etl time to date only
pos_data_count_sort["etl_timestamp"] = pd.to_datetime(pos_data_count_sort["etl_timestamp"])
pos_data_count_sort["etl_timestamp"]= pos_data_count_sort["etl_timestamp"].dt.date

#verify and filter out zips to philadelphia only 
def ZipToCity(x):
    search = SearchEngine(simple_zipcode=True)
    city = search.by_zipcode(x).city
    return city if city else x 
pos_data_count_sort['city'] = pos_data_count_sort['zip_code'].fillna(0).astype(int).astype(str).apply(ZipToCity)
final_cleaned_poscases = pos_data_count_sort[pos_data_count_sort['city'].str.contains("Philadelphia")]

#final table with selected columns
final_cleaned_poscases = final_cleaned_poscases.iloc[:, 0:3]

#take a look at final table 
# print(final_cleaned_poscases)

#create philly map 

# shape_path = r"/Users/yasminayala/Desktop/Philly Covid/data/tl_2019_42101_faces/tl_2019_42101_faces.shp"
shape_path = r"/home/acorn/Projects/PhillyCovidMapping/tl_2019_42101_faces/tl_2019_42101_faces.shp"
philly_map = geopandas.read_file(shape_path)

# get zip code and geometry columns only
pmap = philly_map[["ZCTA5CE10", "geometry"]]

#drop duplicates and rename to match the zip_code column in final_cleaned_poscases
pmap_clean = pmap.drop_duplicates(subset="ZCTA5CE10", keep='first')
pmap_cleaned = pmap_clean.rename(columns={"ZCTA5CE10": "zip_code"})

# convert zip_code column to int64 for the merge
pmap_cleaned["zip_code"] = pd.to_numeric(pmap_cleaned["zip_code"])

# merge geopandas frame pmap_cleaned with pandas dataframe final_cleaned_poscases on "zip_code" column which they both share
merged = pmap_cleaned.merge(final_cleaned_poscases, on="zip_code")

# print(merged)

# plot 
#lots of adjustments need to be made....

variableCount = "count"
fig, ax = plt.subplots(1, figsize=(30, 10))
ax.axis('off')
vmin, vmax = 500, 10000
sm = plt.cm.ScalarMappable(cmap="Blues", norm=plt.Normalize(vmin=vmin, vmax=vmax))

sm.set_array([])

fig.colorbar(sm)

# plt.rcParams["figure.figsize"] = [50,70]
merged.plot(column=variableCount, cmap="Blues", linewidth=0.8, ax=ax,edgecolor="0.8")
plt.show()


#taking a look at the cleaned data 
# print(final_cleaned_poscases.dtypes)
# print(final_cleaned_poscases)
# print(len(final_cleaned_poscases))
# print(len(main_data))





