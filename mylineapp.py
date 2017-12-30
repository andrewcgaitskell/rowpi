# myapp.py

from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.models import ColumnDataSource
from bokeh.palettes import RdYlBu3
from bokeh.palettes import Spectral11
from bokeh.plotting import figure, curdoc

from sqlalchemy import create_engine
import pandas as pd
from pandas.io import sql

# create a plot and style its properties
p = figure(plot_width=400, plot_height=400,x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'white'
p.background_fill_color = 'white'
p.outline_line_color = 'black'
p.grid.grid_line_color = 'black'

def RefreshData():
    engine = create_engine('postgresql://andrew:andrew@localhost:5432/data')

    #sqlcmnd = 'SELECT stroketime, distance, spm, power, pace, calhr, calories, heartrate, status, rowingid FROM strokes.floats;'

    sqlcmnd = 'SELECT stroketime, distance,rowingid FROM strokes.floats;'
    df = pd.read_sql_query(sqlcmnd, engine)

    #print df

    #my_times = df["stroketime"].tolist()
    #my_distances = df["distance"].tolist()

    # add a line renderer
    # p.line(my_times, my_distances, line_width=2)

    #toy_df = pd.DataFrame(data=np.random.rand(5,3), columns = ('a', 'b' ,'c'), index = pd.DatetimeIndex(start='01-01-2015',periods=5, freq='d'))   

    #newx = list(df["stroketime"].groupby(df["rowingid"]))
    #newy = list(df["distance"].groupby(df["rowingid"]))

    newx_out = []
    newy_out = []

    # Group the dataframe by regiment, and for each regiment,
    for stroketime, group in df.groupby('rowingid'): 
        # print the name of the regiment
        # print(name)
        # print the data of that regiment
        my_group_times = group["stroketime"].tolist()
        newx_out.append(my_group_times)

    for distance, group in df.groupby('rowingid'): 
        # print the name of the regiment
        # print(name)
        # print the data of that regiment
        my_group_distances = group['distance'].tolist()
        newy_out.append(my_group_distances)

    listofrows = df['rowingid'].unique()

    numlines=len(listofrows)
    mypalette_out=Spectral11[0:numlines]
    
    return newx_out,newy_out,mypalette_out

#p.multi_line(newx, newy,
#             color=mypalette , line_width=4)

# add a text renderer to our plot (no data yet)
#r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
#           text_baseline="middle", text_align="center")

# create a callback that will add a number in a random location
def callback():
    newx,newy,mypalette = RefreshData()
    source = ColumnDataSource(dict(xs=newx, ys=newx))
    p.multi_line(x='stroketime', y='distance', source=source, color=mypalette , line_width=4)

    

newx,newy,mypalette = RefreshData()
source = ColumnDataSource(data = dict(xs=newx, ys=newx))
r = p.multi_line(x='stroketime', y='distance', source=source, color=mypalette , line_width=4)


# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
