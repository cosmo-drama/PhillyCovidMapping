#imports
from pickle import FALSE
import geopandas
import numpy as np
import pandas as pd
from matplotlib import *
from matplotlib import pyplot as plt
import datetime
from pyzipcode import ZipCodeDatabase
from uszipcode import SearchEngine, SimpleZipcode, Zipcode
# from geopandas import read_file
# import mapclassify
# import libpysal

#configs to print all rows and column
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

#pull in data
path = r"/Users/yasminayala/Desktop/Philly Covid/data/covid_cases_by_zip.csv"
df = pd.read_csv(path)
# print(df['zip_code']['covid_status']['count'])


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
# philly_map = geopandas.read_file(shape_path)
# philly_map.head()


#taking a look at the cleaned data 
# print(final_cleaned_poscases.dtypes)
# print(final_cleaned_poscases)
# print(len(final_cleaned_poscases))
# print(len(main_data))


# pos_data.plot.area(stacked=False)
# plt.show()

# pos_data.plot.pie(subplots=True)
# plt.show()



