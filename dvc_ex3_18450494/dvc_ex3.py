import pandas as pd 
import numpy as np
import bokeh.palettes as bp
from bokeh.plotting import figure, output_notebook
from bokeh.io import output_file, show, save
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, RangeTool
from bokeh.transform import linear_cmap, transform
from bokeh.layouts import gridplot, column


# ==========================================================================
# Goal: Visualize Covid-19 Tests statistics in Switzerland with linked plots
# Dataset: covid19_tests_switzerland_bag.csv
# Data Interpretation: 
# 		n_negative: number of negative cases in tests
# 		n_positive: number of positive cases in tests
# 		n_tests: number of total tests
# 		frac_negative: fraction of POSITIVE cases in tests
# ==========================================================================



### Task1: Data Preprocessing


## T1.1 Read the data to the dataframe "raw"
# You can read the latest data from the url, or use the data provided in the folder (update Nov.3, 2020)

url = 'https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_tests_switzerland_bag.csv'
raw = pd.read_csv(url,index_col=0)
raw.rename(columns={"frac_negative":"frac_positive"}, inplace=True)

## T1.2 Create a ColumnDataSource containing: date, positive number, positive rate, total tests
# All the data can be extracted from the raw dataframe.

date = pd.to_datetime(raw["date"])
pos_num = raw["n_positive"]
pos_rate = raw["frac_positive"]
test_num = raw["n_tests"]


source = ColumnDataSource(data = dict(date = date, pos_num = pos_num, pos_rate = pos_rate, test_num = test_num))

## T1.3 Map the range of positive rate to a colormap using module "linear_cmap"
# "low" should be the minimum value of positive rates, and "high" should be the maximum value

mapper = linear_cmap("pos_rate", palette="Viridis256", low=min(pos_rate), high=max(pos_rate))

#output_notebook()
### Task2: Data Visualization
# Reference link:
# (range tool example) https://docs.bokeh.org/en/latest/docs/gallery/range_tool.html?highlight=rangetool


## T2.1 Covid-19 Total Tests Scatter Plot
# x axis is the time, and y axis is the total test number. 
# Set the initial x_range to be the first 30 days.

TOOLS = "box_select,lasso_select,wheel_zoom,pan,reset,help"
p = figure(plot_width = 1600, plot_height = 650, x_axis_type = "datetime", x_range = (source.data.get("date")[0], source.data.get("date")[30]), tools="")
p.scatter(y = 'test_num', x = 'date', marker = "circle", size = 10, source = source, name = 'test_num', fill_color=mapper, line_color=mapper)

p.title.text = 'Covid-19 Tests in Switzerland'
p.yaxis.axis_label = "Total Tests"
p.xaxis.axis_label = "Date"

# Add a hovertool to display date, total test number
hover = HoverTool(
    tooltips = [
    ("Date", "@date{%F}"),
    ("Total test number", "@$name")]
    ,formatters={'@date': 'datetime'}
)
p.add_tools(hover)



## T2.2 Add a colorbar to the above scatter plot, and encode positve rate values with colors; please use the color mapper defined in T1.3 

color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0,0), title="P-rate")

p.add_layout(color_bar, 'right')


## T2.3 Covid-19 Positive Number Plot using RangeTool
# In this range plot, x axis is the time, and y axis is the positive test number.

select = figure(plot_height = 250, plot_width=1600, x_axis_type="datetime", tools="")

# Define a RangeTool to link with x_range in the scatter plot
range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "green"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'pos_num', source=source, name = 'pos_num')
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

# Draw a line plot and add the RangeTool to the plot
select.yaxis.axis_label = "Positive Cases"
select.xaxis.axis_label = "Date"


# Add a hovertool to the range plot and display date, positive test number
hover2 = HoverTool(
    tooltips = [
    ("Date", "@date{%F}"),
    ("Positive Cases", "@$name")]
    ,formatters={'@date': 'datetime'}
)
select.add_tools(hover2)
show(column(p, select))