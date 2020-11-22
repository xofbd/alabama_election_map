# author: xofbd
# date: December 13, 2017
# file name: process_election_data.py
#
# The purpose of this script is to process the AL election data to visualize
# the results on a county level using Bokeh.

import pandas as pd

# load excel data
df_A = pd.read_excel('sosEnrExport.xlsx', sheetname=0)
df_B = pd.read_excel('sosEnrExport.xlsx', sheetname=1)

# only include senate race
senate_contest_code = 1000900
df_A = df_A.loc[df_A['Contest Code'] == senate_contest_code]

# merge on county code
columns_B = ['County Code', 'Ballots Cast']
df = pd.merge(df_A, df_B[columns_B], on='County Code')
df['Percentage of Vote'] = 100 * df['Votes'] / df['Ballots Cast']

# save DataFrame to csv file
df.to_csv('data/county_level_percentages.csv', delimiter=',')
