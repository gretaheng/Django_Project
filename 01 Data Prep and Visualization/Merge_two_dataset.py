# Merge data output from Modify_csv_data.py and Get_Security_Alert.py

import urllib
import pandas as pd
import certifi
from geopy.geocoders import Nominatim
from urllib.request import urlopen

# install geopy to return location, https://pypi.python.org/pypi/geopy
# Prepare to return location
def uo(args, **kwargs):
    return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)

geolocator = Nominatim()
geolocator.urlopen = uo

# read in csv
security_alert_df = pd.read_csv('security.csv')
security_alert_df = security_alert_df.dropna()

# change data type
security_alert_df["Address"] = security_alert_df["Address"].astype(str)
security_alert_df["Date"] = security_alert_df["Date"].astype(int)
security_alert_df["Time"] = security_alert_df["Time"].astype(int)
security_alert_df["PrimaryType"] = "ROBBERY"

# get latitude and longitude, and store in list
Latitude_list = []
Longitude_list = []
for address in security_alert_df["Address"]:
    try:
        Location = geolocator.geocode(address)
        Latitude = Location.latitude
        Longitude = Location.longitude
        Latitude_list.append(Latitude)
        Longitude_list.append(Longitude)
    except Exception:
        Latitude_list.append('')
        Longitude_list.append('')
        pass

# append latitude and longitude to data frame
Lat = pd.Series(Latitude_list)
security_alert_df['Latitude'] = Lat.values
Long = pd.Series(Longitude_list)
security_alert_df['Longitude'] = Long.values
security_alert_df = security_alert_df[security_alert_df['Latitude'] != '']
security_alert_df = security_alert_df[security_alert_df['Longitude'] != '']

# change string to float
security_alert_df["Latitude"] = security_alert_df["Latitude"].astype(float)
security_alert_df["Longitude"] = security_alert_df["Longitude"].astype(float)

# apply location filter
latitude_filter = (security_alert_df.Latitude >= 41.78013) & \
                  (security_alert_df.Latitude <= 41.809241)
longitude_filter = (security_alert_df.Longitude >= -87.615546) & \
                   (security_alert_df.Longitude <= -87.575706)

security_alert_df = security_alert_df[latitude_filter]
security_alert_df = security_alert_df[longitude_filter]

# import data into pandas data frame
hyde_park = pd.read_csv('hyde_park_crime.csv')

# append two data frames
final_df = hyde_park.append(security_alert_df, ignore_index=True)

# convert string into integer
final_df["Date"] = final_df["Date"].astype(int)

# define useful columns
useful_col = ['Date', 'Time', 'PrimaryType', 'Latitude', 'Longitude', 'Location']
final_df = final_df[useful_col]

# sort values by ('Date', 'Time')
final_df = final_df.sort_values(by=['Date', 'Time'], ascending=True)

# export to csv
final_df.to_csv("Final_data.csv", index=False)
