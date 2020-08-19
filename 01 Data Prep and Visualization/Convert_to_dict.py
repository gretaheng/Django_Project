# Convert the output from Modify_csv_data.py into a dictionary and export as json file

import pandas as pd
import json

# import hyde_park_crime data into pandas data frame
hyde_park = pd.read_csv('hyde_park_crime.csv')

# make all upper case in to lower case
hyde_park = hyde_park.apply(lambda x: x.astype(str).str.lower())

# get data only for 2017
hyde_park = hyde_park[(hyde_park.Year == "2017")]

# convert data frame columns into list
ID = hyde_park["ID"].tolist()
PrimaryType = hyde_park["PrimaryType"].tolist()
X_Coordinate = hyde_park["XCoordinate"].tolist()
Y_Coordinate = hyde_park["YCoordinate"].tolist()

# define a dictionary
hyde_park_list = []
for i in range(len(ID)):
    i = {"type": PrimaryType[i],"geometry": {"type": "Point", "location": (X_Coordinate[i], Y_Coordinate[i])}}
    hyde_park_list.append(i)

# define a dictionary
final_dict = {"features": hyde_park_list}

# drop dictionary key
if 'key' in final_dict:
    del final_dict['key']

# export as a json file
with open('final_dict.json', 'w') as fd:
    json.dump(final_dict, fd)

