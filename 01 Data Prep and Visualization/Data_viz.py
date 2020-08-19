# Use Python Seaborn package to create data visualizations and perform data analysis

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar

sns.set()

# import data into pandas data frame
crime_df = pd.read_csv('hyde_park_crime.csv')

# take out the month data from thr date data
crime_df['Month'] = crime_df['Date'].map(lambda x: str(x)[4:6])

# filter out if year == 2018
crime_df = crime_df[(crime_df.Year < 2018)]

# convert Year, Month, and Time string into int
crime_df["Year"] = crime_df["Year"].astype(int)
crime_df["Month"] = crime_df["Month"].astype(int)
crime_df["Time"] = crime_df["Time"].astype(int)

# create a list for month
month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Rename crime type
Crime_Acronym = {'OTHER OFFENSE':'Offense etc.',
              'LIQUOR LAW VIOLATION': 'Liquor Vio',
              'DECEPTIVE PRACTICE': 'Deceit',
              'INTERFERENCE WITH PUBLIC OFFICER': 'Interference',
              'PUBLIC PEACE VIOLATION': 'Peace Vio',
              'CONCEALED CARRY LICENSE VIOLATION': 'License Vio',
              'NARCOTICS': 'Narcotics',
              'THEFT': 'Theft',
              'STALKING': 'Stalking',
              'INTIMIDATION': 'Intimidation',
              'CRIMINAL DAMAGE': 'Damage',
              'OBSCENITY': 'Obscenity',
              'PUBLIC INDECENCY': 'Indecency',
              'MOTOR VEHICLE THEFT': 'Motor Theft',
              'BURGLARY': 'Burglary',
              'ROBBERY': 'Robbery',
              'ASSAULT': 'Assault',
              'BATTERY': 'Battery',
              'WEAPONS VIOLATION': 'Weapon Vio',
              'KIDNAPPING': 'Kidnapping',
              'CRIM SEXUAL ASSAULT': 'Sexual Vio',
              'SEX OFFENSE': 'Sex Offense',
              'OFFENSE INVOLVING CHILDREN': 'Child Abuse',
              'HOMICIDE': 'Homicide',
              'HUMAN TRAFFICKING': 'Human Traffic',
              'MURDER': 'Murder'}

crime_df['CrimeAcronym'] = crime_df['PrimaryType'].map(Crime_Acronym)


def group_by(dataframe, column1, column2, column3):
    '''
    Data frame group by columns

    Inputs:
        dataframe: pandas data frame
        column1: string, column name
        column2: string, column name
        column3: string, column name

    Returns: data frame
    '''
    new = dataframe.groupby([column1, column2])[column3].count().reset_index(name="count")
    return new


def sort_values(dataframe, column):
    '''
    Sort data frame by column values

    Inputs:
        dataframe: pandas data frame
        column: string, column name

    Returns: data frame
    '''
    new = dataframe.sort_values(column)
    return new


def pivot(dataframe, column1, column2, column3):
    '''
    Pivot data frame by column

    Inputs:
        dataframe: pandas data frame
        column1: string, column name
        column2: string, column name
        column3: string, column name

    Returns: data frame
    '''
    new = dataframe.pivot(column1, column2, column3)
    return new


def fillna(dataframe):
    '''
    Fill none with 0

    Inputs:
        dataframe: pandas data frame

    Returns: data frame
    '''
    new = dataframe.fillna(0)
    return new


def astype_int(dataframe):
    '''
    Data frame column as integer

    Inputs:
        dataframe: pandas data frame

    Returns: data frame
    '''
    new = dataframe.astype(int)
    return new


def time_slot(row):
    '''
    Group time into 12 different time slot

    Inputs:
        row: pandas data frame row

    Returns: string value
    '''
    if 000 <= row['Time'] < 200:
        return '0am-2am'
    if 200 <= row['Time'] < 400:
        return '2am-4am'
    if 400 <= row['Time'] < 600:
        return '4am-6am'
    if 600 <= row['Time'] < 800:
        return '6am-8am'
    if 800 <= row['Time'] < 1000:
        return '8am-10am'
    if 1000 <= row['Time'] < 1200:
        return '10am-12pm'
    if 1200 <= row['Time'] < 1400:
        return '12pm-2pm'
    if 1400 <= row['Time'] < 1600:
        return '2pm-4pm'
    if 1600 <= row['Time'] < 1800:
        return '4pm-6pm'
    if 1800 <= row['Time'] < 2000:
        return '6pm-8pm'
    if 2000 <= row['Time'] < 2200:
        return '8pm-10pm'
    if 2200 <= row['Time'] < 2400:
        return '10pm-12am'
    if row['Time'] >= 2400:
        return '12pm-2pm'

# group time into 12 different time slot
crime_df.apply(lambda row: time_slot (row),axis=1)
crime_df['Time Slot'] = crime_df.apply(lambda row: time_slot (row), axis=1)


# figure 1 -- month and year overall
def crime1():
    crime_1 = group_by(crime_df, "Year", "Month", "ID")
    crime_1 = sort_values(crime_1, "Month")
    crime_1['Month'] = crime_1['Month'].apply(lambda x: calendar.month_abbr[x])
    crime_1 = pivot(crime_1, "Year", "Month", "count")
    crime_1 = crime_1[month_list]
    return crime_1

def heat_map_1(dataframe):
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(dataframe, annot=True, fmt="d", linewidths=.5, ax=ax, cmap="YlOrRd")
    ax.invert_yaxis()
    map.set_title('Count for Crime by Month, 2013 - 2017', fontsize=20)
    map.figure.savefig("Count for Crime by Month, 2013 - 2017.png", format='png', dpi=1000)

figure_1 = heat_map_1(crime1())


# figure 2 -- primary crime type and year overall
def crime_2():
    crime_2 = group_by(crime_df, "Year", "CrimeAcronym", "ID")
    crime_2 = pivot(crime_2, "Year", "CrimeAcronym", "count")
    crime_2 = fillna(crime_2)
    crime_2 = astype_int(crime_2)
    crime_2 = crime_2.reindex(sorted(crime_2.columns, key=lambda x: crime_2[x][2017]), axis=1)
    cols = (crime_2 >= 2).any()
    crime_2 = crime_2[cols[cols].index]
    return crime_2

def heat_map_2(dataframe):
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(dataframe, annot=True, fmt="d", linewidths=.5, ax=ax, cmap="YlOrRd")
    sns.set(font_scale=0.7)
    ax.invert_yaxis()
    map.set_title('Count for Crime by Primary Crime Type, 2013 - 2017',fontsize=20)
    map.figure.savefig("Count for Crime by Primary Crime Type, 2013 - 2017.png", format='png', dpi=1000)

figure_2 = heat_map_2(crime_2())


# figure 3 -- aggregate crime type and year overall
def crime_3():
    crime_3 = group_by(crime_df, "Year", "AggregateType", "ID")
    crime_3 = pivot(crime_3, "Year", "AggregateType", "count")
    crime_3 = fillna(crime_3)
    crime_3 = astype_int(crime_3)
    return crime_3

def heat_map_3(dataframe):
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(dataframe, annot=True, fmt="d", linewidths=.5, ax=ax, cmap="YlOrRd")
    ax.invert_yaxis()
    map.set_title('Count for Crime by Aggregate Crime Type, 2013 - 2017',fontsize=20)
    map.figure.savefig("Count for Crime by Aggregate Crime Type, 2013 - 2017.png", format='png', dpi=1000)

figure_3 = heat_map_3(crime_3())


# Graph 4 -- each year and am/pm
def crime_4():
    crime_4 = sort_values(crime_df, "Time")
    return crime_4

def histogram_1(column, dataframe):
    hist = sns.factorplot(x=column, data=dataframe, kind="count",
                       palette="BuPu", size=6, aspect=1.5)
    sns.set(font_scale=1)
    hist.set_xticklabels(step=2)
    plt.subplots_adjust(top=0.9)
    hist.fig.suptitle('Count for Crime by Time Slot, 2013 - 2017', fontsize=20)
    hist.savefig("Count for Crime by Time Slot, 2013 - 2017.png", format='png', dpi=1000)

figure_4 = histogram_1("Time Slot", crime_4())


def heat_map(dataframe):
    '''
    draw heap map

    Inputs:
        row: pandas data frame

    Returns: figure
    '''
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(dataframe, annot=True, fmt="d", linewidths=.5, ax=ax, cmap="YlOrRd")
    map.set_title('Heat Map', fontsize=20)
    sns.set(font_scale=0.7)
    return map


def sub_heat_map(year, dataframe, column):
    '''
    format data frame to draw sub heat map

    Inputs:
        year: int, the only year to keep
        dataframe: pandas data frame
        column: string, column name

    Returns: figure
    '''
    crime_df_by_year = dataframe[(crime_df.Year == year)]
    crime_df_by_year = group_by(crime_df, "Month", column, "ID")
    crime_df_by_year['Month'] = crime_df_by_year['Month'].apply(lambda x: calendar.month_abbr[x])
    crime_df_by_year = pivot(crime_df_by_year, column, "Month", "count")
    crime_df_by_year = fillna(crime_df_by_year)
    crime_df_by_year = astype_int(crime_df_by_year)
    crime_df_by_year = crime_df_by_year[month_list]

    map = heat_map(crime_df_by_year)
    return map


def hist_by_year(dataframe, year):
    '''
    draw histogram

    Inputs:
        row: pandas data frame
        year: int, the only year to keep

    Returns: figure
    '''
    crime_df_by_year = dataframe[(dataframe.Year == year)]
    crime_df_by_year = sort_values(crime_df_by_year, "Time")
    hist = sns.factorplot(x="Time Slot", data=crime_df_by_year, kind="count",
                       palette="BuPu", size=6, aspect=1.5)
    hist.set_xticklabels(step=2)
    plt.subplots_adjust(top=0.9)
    hist.fig.suptitle("Histogram", fontsize=20)
    return hist


# sub_figure 2 -- primary crime type by year
heat_map_2_2013 = sub_heat_map(2013, crime_df, "CrimeAcronym")
heat_map_2_2014 = sub_heat_map(2014, crime_df, "CrimeAcronym")
heat_map_2_2015 = sub_heat_map(2015, crime_df, "CrimeAcronym")
heat_map_2_2016 = sub_heat_map(2016, crime_df, "CrimeAcronym")
heat_map_2_2017 = sub_heat_map(2017, crime_df, "CrimeAcronym")

# sub_figure 3 -- aggregate crime type by year
heat_map_3_2013 = sub_heat_map(2013, crime_df, "AggregateType")
heat_map_3_2014 = sub_heat_map(2014, crime_df, "AggregateType")
heat_map_3_2015 = sub_heat_map(2015, crime_df, "AggregateType")
heat_map_3_2016 = sub_heat_map(2016, crime_df, "AggregateType")
heat_map_3_2017 = sub_heat_map(2017, crime_df, "AggregateType")

# sub_figure 4 --  am/pm by year
hist_2013 = hist_by_year(crime_df, 2013)
hist_2014 = hist_by_year(crime_df, 2014)
hist_2015 = hist_by_year(crime_df, 2015)
hist_2016 = hist_by_year(crime_df, 2016)
hist_2017 = hist_by_year(crime_df, 2017)

