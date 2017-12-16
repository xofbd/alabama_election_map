# author: xofbd
# date: December 15, 2017
# file name: bokeh_plot.m

from matplotlib import cm
import pandas as pd
import pickle

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    ColorBar
)


def rgb_to_hex(cmap):
    '''Return list of color hex codes given a matplotlib colormap.'''
    hex = []
    N = 255

    for i in xrange(N):
        r, g, b, a = getattr(cm, cmap)(i)
        hex.append('#%02x%02x%02x' % (N * r, N * g, N * b))

    return hex


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


def create_plot():

    # get county lats, lons, and county names
    with open('data/counties.p', 'r') as fp:
        counties = pickle.load(fp)

    county_xs = [county['lons'] for county in counties.values()]
    county_ys = [county['lats'] for county in counties.values()]
    county_names = [county['name'] for county in counties.values()]

    # get processed election data and store as ColumnDataSource
    df = pd.read_csv('data/county_level_percentages.csv', delimiter=',')
    dem_pct = get_pct(df, county_names, 'DEM')
    rep_pct = get_pct(df, county_names, 'REP')
    wrt_pct = get_pct(df, county_names, 'NON')

    source = ColumnDataSource(data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        dem_pct=dem_pct,
        rep_pct=rep_pct,
        wrt_pct=wrt_pct
    ))

    # set colormap
    palette = rgb_to_hex('seismic')
    palette.reverse()

    color_mapper = LinearColorMapper(palette=palette, low=0, high=100)
    color_bar = ColorBar(color_mapper=color_mapper,
                         border_line_color=None, location=(15, 0), label_standoff=0)

    # initialize figure object
    TOOLS = "pan, wheel_zoom, reset, hover, save"

    p = figure(
        title="Alabama US Senate Special Election 2017", tools=TOOLS,
        x_axis_location=None, y_axis_location=None
    )
    p.grid.grid_line_color = None

    # add county shapes and color to the patches
    p.patches('x', 'y', source=source,
              fill_color={'field': 'dem_pct', 'transform': color_mapper},
              fill_alpha=1.0, line_color="white", line_width=0.5)

    # display color bar
    p.add_layout(color_bar, 'right')

    # add hover with fields to display
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("County", "@name"),
        ("Doug Jones", "@dem_pct%"),
        ("Roy Moore", "@rep_pct%"),
        ("Write In", "@wrt_pct%"),
        ("(Long, Lat)", "($x, $y)"),
    ]

    return components(p)

if __name__ == '__main__':
    create_plot()
