# author: xofbd
# date: December 17, 2017
# file name: get_election_results_2016.py
#
# The purpose of this script is to obtain the 2016 presidential election
# results from wikipedia, using web scraping with BeautifulSoup

from bs4 import BeautifulSoup
from urllib2 import urlopen


def get_data(url):

    # create soup object for scrapping
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    # get table and td tags
    table = soup.find('table', 'wikitable sortable')
    td_tags = table.find_all('td')

    # strip data/info from td tags and dump to a dictionary
    data_dict = {}
    col_names = (
        'county', 'djt_votes', 'djt_pct', 'hrc_votes', 'hrc_pct', 'gej_votes',
        'gej_pct', 'jes_votes', 'jes_pct', 'wrt_votes', 'wrt_pct', 'total_votes', 'total_turnout'
    )

    n_cols = len(col_names)
    n_tags = len(td_tags)

    for i, col in enumerate(col_names):
        if col == 'county':
            data_dict[col] = [
                td_tags[i].a.text for i in xrange(i, n_tags, n_cols)]
        else:
            data_dict[col] = [
                td_tags[i].text for i in xrange(i, n_tags, n_cols)]

    return data_dict

if __name__ == '__main__':
    import pandas as pd

    url = 'https://en.wikipedia.org/wiki/United_States_presidential_election_in_Alabama,_2016'

    data_dict = get_data(url)

    # dump data into csv file
    df = pd.DataFrame(data_dict)
    df.to_csv('data/alabama_presidential_election_2016.csv', sep=',')
