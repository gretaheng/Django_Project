# Divide the data into twenty-four subsets
# Xi Chen
# Original code


import csv
import pandas as pd

def subset_crime_df(df):
    ''' 
    Seperate the complete dataset into several subsets by hours. For example, 
    "time_0_100.csv" refers to the subset of the crime happened between 
    0 am - 1 am. In these csv files, the first row is the location:(lat, lng),
    the second row is a crime weight(the dangerous score) for this location.

    Inputs:
        df: (dataframe) all the crime data with 

    Returns: several csv files for crime happened in different hours
    '''

    for i in range(24):
        sub_df = df[(df.Time >= i*100) & (df.Time < (i*100 + 100))]
        loc_ls = sub_df.Location.unique()
        
        loc_score = {}
        for location in loc_ls:
            l = location[1:-1].split(',')
            loc = float(l[0]), float(l[1])
            total_s = df[df.Location == location]['weight'].sum()
            loc_score[loc] = total_s
        loc_score = dict(sorted(loc_score.items()))
        
        csv_file = './Data/time_' + str(i*100) + '-' + str(i*100 + 100) + '.csv'
        
        with open(csv_file, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            for key, val in loc_score.items():
                spamwriter.writerow([key, val])


if __name__ == "__main__":

    df = pd.read_csv('./Data/data_with_weight.csv')
    subset_crime_df(df)



