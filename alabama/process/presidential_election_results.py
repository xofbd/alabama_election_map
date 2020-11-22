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


def process_data(td_tags):
    """Return dictionary containing processed data from table data."""
    col_names = ('county', 'djt_votes', 'djt_pct', 'hrc_votes', 'hrc_pct',
                 'gej_votes', 'gej_pct', 'jes_votes', 'jes_pct', 'wrt_votes',
                 'wrt_pct', 'total_votes', 'total_turnout')

    n_cols = len(col_names)
    n_tags = len(td_tags)
    n_rows = n_tags // n_cols

    def process_row(tags):
        return dict(zip(col_names, [tag.text.strip() for tag in tags]))

    return [process_row(td_tags[i*n_cols:(i+1)*n_cols]) for i in range(n_rows)]


def dump_data(data, path):
    """Dump data object to disk as CSV file."""
    pd.DataFrame(data).to_csv(path, index=False)


def main(url, path):
    td_tags = scrape_table_data(url)
    election_data = process_data(td_tags)
    dump_data(election_data, path)


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/w/index.php?title=2016_United_States_presidential_election_in_Alabama&oldid=814157769'
    path = os.path.join('data', 'alabama_presidential_election_2016.csv')
    main(url, path)
