import pandas as pd

from bokeh.embed import components
from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    ColorMapper
)

from bokeh.palettes import RdYlBu as palette
# from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure

palette = palette[11]


def create_plot():
    palette.reverse()

    with open('data/counties.p', 'r') as fp:
        counties = pickle.load(fp)

    county_xs = [county['lons'] for county in counties.values()]
    county_ys = [county['lats'] for county in counties.values()]

    county_names = [county['name'] for county in counties.values()]

    # get election data
    df = pd.read_csv('data/county_level_percentages.csv', delimiter=',')
    county_rates = [df.loc[(df['County Name'] == county) & (df['Party Code'] == 'DEM')]['Percentage of Vote'].values[0]
                    for county in county_names]

    # county_rates = [unemployment[county_id] for county_id in counties]
    color_mapper = ColorMapper(palette=palette)

    source = ColumnDataSource(data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        rate=county_rates,
    ))

    TOOLS = "pan, wheel_zoom, reset, hover, save"

    p = figure(
        title="Alabama US Senate Special Election 2017", tools=TOOLS,
        x_axis_location=None, y_axis_location=None
    )
    p.grid.grid_line_color = None

    p.patches('x', 'y', source=source,
              fill_color={'field': 'rate', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)

    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Name", "@name"),
        ("Doug Jones", "@rate%"),
        ("(Long, Lat)", "($x, $y)"),
    ]
    # return unemployment
    # show(p)
    # return components(p)


create_plot()

# need list of lats, longs, names, percentage
