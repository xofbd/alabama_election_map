"""
The purpose of this script is to process the AL election data to visualize the
results on a county level using Bokeh. Each row represents a different county
with the percentages each candidate received.
"""
import os

import pandas as pd


def main(path_in, path_out):
    """
    Dump special senate race election data to disk as a CSV.

    The passed path of the data contains Alabama election data, more than just
    the 2017 special senate election race data. This function reads the Excel
    file and creates a CSV file of the relevant data needed to visualize the
    results.
    """

    # Data frame where each row contains voting results for each county and
    # candidate
    df_A = pd.read_excel(path_in, sheet_name=0)
    df_B = pd.read_excel(path_in, sheet_name=1)

    senate_contest_code = 1000900
    columns_B = ['County Code', 'Ballots Cast']

    df = (df_A.query('`Contest Code` == @senate_contest_code')
              .merge(df_B[columns_B], on='County Code'))
    df['Percentage of Vote'] = 100 * df['Votes'] / df['Ballots Cast']

    # Data frame where each row contains the voting results for each county
    (df.pivot(index='County Name',
              values='Percentage of Vote',
              columns='Candidate Name')
     .fillna(0).to_csv(path_out, index=True))


if __name__ == '__main__':
    path_in = os.path.join('data', 'sosEnrExport.xlsx')
    path_out = os.path.join('data', 'senate_election_results.csv')
    main(path_in, path_out)
