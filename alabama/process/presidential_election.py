"""
The purpose of this script is to obtain the 2016 presidential election results
through scraping the appropriate Wikipedia article.
"""
import os

from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape_table_data(url):
    """Return list of td tags from scraping URL."""
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    return soup.select('table.wikitable.sortable td')


def create_data_frame(td_tags):
    """Return data frame containing processed data from the table data."""
    col_names = ('County Name', 'DJT Votes', 'DJT pct', 'HRC Votes', 'HRC pct',
                 'GEJ Votes', 'GEJ pct', 'JES Votes', 'JES pct', 'WRT Votes',
                 'WRT pct', 'Total Votes', 'Total Turnout')

    n_cols = len(col_names)
    n_tags = len(td_tags)
    n_rows = n_tags // n_cols

    def process_row(tags):
        return dict(zip(col_names, [tag.text.strip() for tag in tags]))

    data = [process_row(td_tags[i*n_cols:(i+1)*n_cols]) for i in range(n_rows)]
    df = pd.DataFrame(data)
    pct_cols = ['HRC pct', 'DJT pct', 'GEJ pct', 'JES pct']
    df[pct_cols] = df[pct_cols].applymap(lambda pct: float(pct[:-1]))

    return df


def main(url, path):
    td_tags = scrape_table_data(url)
    df = create_data_frame(td_tags)
    df.to_csv(path, index=False)


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/w/index.php?title=2016_United_States_presidential_election_in_Alabama&oldid=814157769'
    path = os.path.join('data', 'presidential_election_results.csv')
    main(url, path)
