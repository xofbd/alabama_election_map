# author: xofbd
# date: December 15, 2017
# file name: bokeh_plot.m

import pandas as pd
import pickle

from bokeh.embed import components
from bokeh.io import show
from bokeh.models import (ColorBar, ColumnDataSource, HoverTool,
                          LinearColorMapper)
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure
from matplotlib import cm


def rgb_to_hex(cmap):
    '''Return list of color hex codes given a matplotlib colormap.'''

    hex_code = []
    N = 255

    for i in xrange(N):
        r, g, b, a = getattr(cm, cmap)(i)
        hex_code.append('#%02x%02x%02x' % (N * r, N * g, N * b))

    return hex_code


def get_pct(df, county_names, party_code):
    '''Return percentage of votes by a given party.'''

    pct = []

    for county in county_names:
        try:
            a = df['County Name'] == county
            b = df['Party Code'] == party_code
            pct.append(df.loc[a & b]['Percentage of Vote'].values[0])
        except:
            pct.append(0)

    return pct


def get_shape_data():
    '''Return county names and coordinates for county patches.'''

    with open('data/counties.p', 'r') as fp:
        counties = pickle.load(fp)

    county_xs = [county['lons'] for county in counties.values()]
    county_ys = [county['lats'] for county in counties.values()]
    county_names = [county['name'] for county in counties.values()]

    return county_names, county_xs, county_ys


def create_map(source, title, hover_list):
    '''Return bokeh Figure object for given election map data.

    Parameters
    ----------
    source : ColumnDataSource
        contains the necessary data to create the county patches.

    title: str
        string of the title for the map.

    hover_list: list
        list of what data to display when hovering over county.

    Returns
    -------
    bokeh Figure object of the map
    '''

    # set colormap
    palette = rgb_to_hex('seismic')
    palette.reverse()

    color_mapper = LinearColorMapper(palette=palette, low=0, high=100)
    color_bar = ColorBar(color_mapper=color_mapper,
                         border_line_color=None, location=(0, 0),
                         label_standoff=5)

    # initialize figure object
    TOOLS = 'pan, wheel_zoom, reset, hover, save'
    plot = figure(title=title, tools=TOOLS, toolbar_location='left',
                  x_axis_location=None, y_axis_location=None, plot_width=450,
                  plot_height=600)
    plot.grid.grid_line_color = None

    # add county shapes and color to the patches
    plot.patches('x', 'y', source=source,
                 fill_color={'field': 'dem_pct', 'transform': color_mapper},
                 fill_alpha=1.0, line_color="white", line_width=1.0)

    # display color bar
    plot.add_layout(color_bar, 'right')

    # add hover with fields to display
    hover = plot.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = hover_list

    return plot


def create_plot(output='components'):

    county_names, county_xs, county_ys = get_shape_data()

    # create appropriate variables for creating 2017 map
    df = pd.read_csv('data/county_level_percentages.csv', delimiter=',')
    dem_pct_2017 = get_pct(df, county_names, 'DEM')
    rep_pct_2017 = get_pct(df, county_names, 'REP')
    wrt_pct_2017 = get_pct(df, county_names, 'NON')

    s1 = ColumnDataSource(data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        dem_pct=dem_pct_2017,
        rep_pct=rep_pct_2017,
        wrt_pct=wrt_pct_2017
    ))

    h1_data = [
        ("County", "@name"),
        ("Doug Jones", "@dem_pct%"),
        ("Roy Moore", "@rep_pct%"),
        ("Write In", "@wrt_pct%"),
        ("(Long, Lat)", "($x, $y)"),
    ]

    # create appropriate variables for creating 2017 map
    df_2016 = pd.read_csv('data/alabama_presidential_election_2016.csv')
    df_2016.set_index('county', inplace=True)

    pct_2016 = dict()
    party_to_cand = {'dem': 'hrc_pct', 'rep':
                     'djt_pct', 'ind': 'gej_pct', 'grn': 'jes_pct'}

    for party, cand in party_to_cand.items():
        pct_2016[party] = [float(df_2016.loc[county, cand][:-1])
                           for county in county_names]

    s2 = ColumnDataSource(data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        dem_pct=pct_2016['dem'],
        rep_pct=pct_2016['rep'],
        ind_pct=pct_2016['ind'],
        grn_pct=pct_2016['grn']
    ))

    h2_data = [
        ("County", "@name"),
        ("Hillary Clinton", "@dem_pct%"),
        ("Donald Trump", "@rep_pct%"),
        ("Gary Johnson", "@ind_pct%"),
        ("Jill Stein", "@grn_pct%"),
        ("(Long, Lat)", "($x, $y)"),
    ]

    p1 = create_map(s1, "Alabama US Senate Special Election 2017", h1_data)
    p2 = create_map(s2, "Alabama US Presidential Election 2016", h2_data)

    # place Figure objects into tabs and return result
    tab1 = Panel(child=p1, title='2017')
    tab2 = Panel(child=p2, title='2016')
    tabs = Tabs(tabs=[tab1, tab2])

    if output == 'show':
        return show(tabs)
    else:
        return components(tabs)

if __name__ == '__main__':
    create_plot(output='show')
