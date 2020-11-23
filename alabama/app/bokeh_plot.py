import json
import os

import pandas as pd
from bokeh.embed import components
from bokeh.io import show
from bokeh.models import (ColorBar, ColumnDataSource, HoverTool,
                          LinearColorMapper)
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure
from matplotlib import cm


def rgb_to_hex(cmap, N=255):
    """Return list of color hex codes given a matplotlib colormap."""

    colormap = getattr(cm, cmap)

    def hex_code(i):
        rgba = map(lambda x: int(N * x), colormap(i))
        return '#%02x%02x%02x' % tuple(rgba)[:-1]

    return [hex_code(i) for i in range(N)]


def get_shape_data():
    """Return county names and coordinates for county patches."""

    with open(os.path.join('data', 'county_shapes.json'), 'r') as f:
        counties = json.load(f)

    return pd.DataFrame(counties).set_index('name')


def create_map(source, title, hover_list):
    """
    Return bokeh Figure object for given election map data.

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
    """

    # Set color map
    palette = rgb_to_hex('seismic')
    palette.reverse()

    color_mapper = LinearColorMapper(palette=palette, low=0, high=100)
    color_bar = ColorBar(color_mapper=color_mapper,
                         border_line_color=None,
                         location=(0, 0),
                         label_standoff=5)

    # Initialize figure object
    TOOLS = 'pan, wheel_zoom, reset, hover, save'
    plot = figure(title=title,
                  tools=TOOLS,
                  toolbar_location='left',
                  x_axis_location=None,
                  y_axis_location=None,
                  plot_width=450,
                  plot_height=600)
    plot.grid.grid_line_color = None

    # Add county shapes and color to the patches
    plot.patches('x', 'y',
                 source=source,
                 fill_color={'field': 'dem_pct', 'transform': color_mapper},
                 fill_alpha=1.0,
                 line_color="white",
                 line_width=1.0)

    # Display color bar
    plot.add_layout(color_bar, 'right')

    # Add hover with fields to display
    hover = plot.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = hover_list

    return plot


def create_plot(output='components'):

    # Create appropriate variables for creating senate election map
    path_senate = os.path.join('data', 'senate_election_county_results.csv')
    df_senate = pd.read_csv(path_senate)
    df_county = get_shape_data()
    df_senate = df_senate.merge(df_county,
                                left_on='County Name',
                                right_index=True)

    s1 = ColumnDataSource(df_senate)
    h1_data = [
        ("County", "@name"),
        ("Doug Jones", "@dem_pct%"),
        ("Roy Moore", "@rep_pct%"),
        ("Write In", "@wrt_pct%"),
        ("(Long, Lat)", "($x, $y)"),
    ]

    # Create appropriate variables for creating presidential election map
    df = (pd.read_csv(os.path.join('data',
                                   'alabama_presidential_election_2016.csv'))
          .set_index('county'))
    df[['hrc_pct', 'djt_pct', 'gej_pct', 'jes_pct']] = df[['hrc_pct', 'djt_pct', 'gej_pct', 'jes_pct']].applymap(
        lambda pct: float(pct[:-1]))

    df = df.rename({'djt_pct': 'rep_pct', 'hrc_pct': 'dem_pct',
                    'gej_pct': 'ind_pct', 'jes_pct': 'grn_pct'})
    df = df.merge(df_county, left_on='county', right_index=True)
    s2 = ColumnDataSource(df)

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

    # TODO: Better way to handle this? Env. variables?
    # df.to_json('df.json')
    if output == 'show':
        return show(tabs)
    else:
        return components(tabs)


if __name__ == '__main__':
    create_plot(output='show')
