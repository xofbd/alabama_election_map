import json
import os

import pandas as pd
from bokeh.embed import components
from bokeh.io import show
from bokeh.models import (ColorBar, ColumnDataSource, HoverTool,
                          LinearColorMapper)
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure


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
    with open(os.path.join('data', 'seismic_colormap.json'), 'r') as f:
        palette = json.load(f)

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


def process_source(path, df_county, dem_candidate):
    """Return ColumnDataSource object for a given election data path."""

    # Since the visualization excepts a uniform name for the field to used for
    # coloring in the map, the percentage the Democratic candidate receives
    # needs to be renamed to dem_pct.
    df_senate = (pd.read_csv(path)
                 .merge(df_county, left_on='County Name', right_index=True)
                 .rename({dem_candidate: 'dem_pct'}, axis=1))

    return ColumnDataSource(df_senate)


def create_plot(output='components'):
    """
    Visualize Alabama election results for presidential and senate races.

    The presidential election is for 2016 while the senate race was the special
    election that occurred in December 2017.
    """

    # Process data for maps
    path_pres = os.path.join('data', 'presidential_election_results.csv')
    path_senate = os.path.join('data', 'senate_election_results.csv')
    df_county = get_shape_data()
    s_1 = process_source(path_senate, df_county, 'Doug Jones')
    s_2 = process_source(path_pres, df_county, 'HRC pct')

    h1_data = [
        ("County", "@{County Name}"),
        ("Doug Jones", "@dem_pct%"),
        ("Roy Moore", "@{Roy S. Moore}%"),
        ("Write In", "@{Write-In}%"),
        ("(Long, Lat)", "($x, $y)"),
    ]

    h2_data = [
        ("County", "@{County Name}"),
        ("Hillary Clinton", "@dem_pct%"),
        ("Donald Trump", "@{DJT pct}%"),
        ("Gary Johnson", "@{GEJ pct}%"),
        ("Jill Stein", "@{JES pct}%"),
        ("(Long, Lat)", "($x, $y)"),
    ]

    p_1 = create_map(s_1, "Alabama US Senate Special Election 2017", h1_data)
    p_2 = create_map(s_2, "Alabama US Presidential Election 2016", h2_data)

    # Place Figure objects into tabs
    tab_1 = Panel(child=p_1, title='2017')
    tab_2 = Panel(child=p_2, title='2016')
    tabs = Tabs(tabs=[tab_1, tab_2])

    if output == 'show':
        return show(tabs)
    elif output == 'components':
        return components(tabs)
    else:
        msg = f"output must be equal to show of components, not {output}."
        raise ValueError(msg)


if __name__ == '__main__':
    create_plot(output='show')
