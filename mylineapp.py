# myapp.py

from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

from sqlalchemy import create_engine
import pandas as pd
from pandas.io import sql

# create a plot and style its properties
p = figure(plot_width=400, plot_height=400,x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'white'
p.background_fill_color = 'red'
p.outline_line_color = 'black'
p.grid.grid_line_color = 'black'

engine = create_engine('postgresql://andrew:andrew@localhost:5432/data')

#sqlcmnd = 'SELECT stroketime, distance, spm, power, pace, calhr, calories, heartrate, status, rowingid FROM strokes.floats;'

sqlcmnd = 'SELECT stroketime, distance,rowingid FROM strokes.floats;'
df = pd.read_sql_query(sqlcmnd, engine)

#print df

my_times = df["stroketime"].tolist()
my_distances = df["distance"].tolist()

# add a line renderer
# p.line(my_times, my_distances, line_width=2)

#toy_df = pd.DataFrame(data=np.random.rand(5,3), columns = ('a', 'b' ,'c'), index = pd.DatetimeIndex(start='01-01-2015',periods=5, freq='d'))   

#newx = list(df["stroketime"].groupby(df["rowingid"]))
#newy = list(df["distance"].groupby(df["rowingid"]))

newx = []
newy = []

# Group the dataframe by regiment, and for each regiment,
for stroketime, group in df.groupby('rowingid'): 
    # print the name of the regiment
    # print(name)
    # print the data of that regiment
    my_group_times = group["stroketime"].tolist()
    newx.append(my_group_times)

for distance, group in df.groupby('rowingid'): 
    # print the name of the regiment
    # print(name)
    # print the data of that regiment
    my_group_distances = group['distance'].tolist()
    newy.append(my_group_distances)
    
p.multi_line(newx, newy,
             color=["firebrick"], alpha=[0.8], line_width=4)

# add a text renderer to our plot (no data yet)
r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
           text_baseline="middle", text_align="center")

i = 0

ds = r.data_source

# create a callback that will add a number in a random location
def callback():
    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds.data['x'] + [random()*70 + 15]
    new_data['y'] = ds.data['y'] + [random()*70 + 15]
    new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i%3]]
    new_data['text'] = ds.data['text'] + [str(i)]
    ds.data = new_data

    i = i + 1

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
