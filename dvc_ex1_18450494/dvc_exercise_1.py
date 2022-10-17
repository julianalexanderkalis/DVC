import pandas as pd 
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS
# import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined
### Task 1: Data Preprocessing
## T1.1 Read online .csv file into a dataframe using pandas
# Reference links: 
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# https://stackoverflow.com/questions/55240330/how-to-read-csv-file-from-github-using-pandas 

original_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics_switzerland_bag.csv'
raw_url = "https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/demographics_switzerland_bag.csv"
dataset = pd.read_csv(raw_url, sep=",", index_col=0)
#print(dataset.shape)

## T1.2 Prepare data for a grouped vbar_stack plot
# Reference link, read first before starting: 
# https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked-and-grouped

# Filter out rows containing 'CH' 
dataset = dataset[dataset["canton"] != "CH"]
#print(dataset.shape)

# Extract unique value lists of canton, age_group and sex
canton = [i for i in dataset["canton"].unique()]
#print(canton)
age_group = [i for i in dataset["age_group"].unique()]
#print(age_group)
sex = [i for i in dataset["sex"].unique()]
#print(sex)

# Create a list of categories in the form of [(canton1,age_group1), (canton2,age_group2), ...]
factors = [(c, a) for c in canton for a in age_group]

# Use genders as stack names
stacks = ['male','female']

# Calculate total population size as the value for each stack identified by canton,age_group and sex
grouped_dataframe = dataset.groupby(["canton", "age_group", "sex"])
male_stack = [grouped_dataframe.get_group((c, a, "Männlich"))["pop_size"].sum() for c in canton for a in age_group]

stack_val = [[grouped_dataframe.get_group((c, a, "Männlich"))["pop_size"].sum() for c in canton for a in age_group], [grouped_dataframe.get_group((c, a, "Weiblich"))["pop_size"].sum() for c in canton for a in age_group]]

# Build a ColumnDataSource using above information
source = ColumnDataSource(data = dict(x = factors, 
                                      male = stack_val[0], 
                                      female = stack_val[1])
                         )

### Task 2: Data Visualization
## T2.1: Visualize the data using bokeh plot functions

from bokeh.plotting import figure, output_file, show, output_notebook

p = figure(x_range = FactorRange(*factors), plot_height = 500, plot_width = 800, title = 'Canton Population Visualization')
p.yaxis.axis_label = "Population Size"
p.xaxis.axis_label = "Canton"
#p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None


p.vbar_stack(stacks, 
             x = "x", 
             source = source, 
             color = ["green", "blue"], 
             width = 0.5, 
             alpha = 0.3,
             legend_label = stacks,
             name = stacks)
## T2.2 Add the hovering tooltips to the plot using HoverTool
# To be specific, the hover tooltips should display “gender”, canton, age group”, and “population” when hovering.
# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# read more if you want to create fancy hover text: https://stackoverflow.com/questions/58716812/conditional-tooltip-bokeh-stacked-chart


hover = HoverTool(tooltips = [
    ("gender", "$name"),
    ("Canton, age group", "@x"),
    ("population", "@$name"),
    ])
p.add_tools(hover)
output_file(filename="18_450_494.html")
show(p)
