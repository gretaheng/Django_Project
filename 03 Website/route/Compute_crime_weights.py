# Compute Crime Weights
# Xi Chen
# Original code


import csv
import pandas as pd
import numpy as np
import re
import string

# Assign different weights for various crime types
CRIME_TYPE = {'DECEPTIVE PRACTICE': 200,
              'THEFT': 200,
              'MOTOR VEHICLE THEFT': 200,
              'CRIMINAL DAMAGE': 200,
              'BURGLARY': 200,
              'ROBBERY': 200,
              'INTERFERENCE WITH PUBLIC OFFICER': 300,
              'PUBLIC PEACE VIOLATION': 300,
              'CONCEALED CARRY LICENSE VIOLATION': 300,
              'NARCOTICS': 300,
              'OTHER OFFENSE':  300,
              'LIQUOR LAW VIOLATION': 300,
              'KIDNAPPING': 300,
              'INTIMIDATION': 300,
              'WEAPONS VIOLATION': 300,
              'STALKING': 400,
              'ASSAULT': 400,
              'BATTERY': 400,
              'CRIM SEXUAL ASSAULT': 400,
              'OFFENSE INVOLVING CHILDREN': 400,
              'HOMICIDE': 400,
              'MURDER': 400,
              'HUMAN TRAFFICKING': 500,
              'OBSCENITY': 500,
              'PUBLIC INDECENCY': 500,
              'SEX OFFENSE': 500,
}


if __name__ == "__main__":

    # Read Crime data
    df = pd.read_csv('./Data/Final_data.csv')

    df['type_weight'] = df['PrimaryType'].map(CRIME_TYPE)

    # Assign different weights for various Crime Date
    date_num_dict = df.groupby(['Date']).size().to_dict()
    date_ls = [*date_num_dict]

    date_dist = {}
    i = 1
    for date in date_ls:
        date_dist[date] = ((i / len(date_ls))**2) * 1000
        i += 1

    df['date_weight'] = df['Date'].map(date_dist)

    # Compute the toal weight for each unique crime location
    df['weight'] = df.type_weight * df.date_weight
    df.to_csv('./Data/data_with_weight.csv', index=False)

