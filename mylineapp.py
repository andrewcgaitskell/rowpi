# myapp.py

from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.models import Plot
from bokeh.models import LinearAxis
from bokeh.models import Grid
from bokeh.models import DataRange1d
from bokeh.models import ColumnDataSource
from bokeh.palettes import RdYlBu3
from bokeh.palettes import Spectral11
from bokeh.plotting import figure, curdoc
from bokeh.models.glyphs import MultiLine
from bokeh.models.glyphs import Line
from bokeh.io import curdoc, show
from bokeh.plotting import reset_output

from sqlalchemy import create_engine
import pandas as pd
from pandas.io import sql

engine = create_engine('postgresql://andrew:andrew@localhost:5432/data')

#sqlcmnd = 'SELECT stroketime, distance, spm, power, pace, calhr, calories, heartrate, status, rowingid FROM strokes.floats;'

sqlcmnd = 'SELECT stroketime, distance,rowingid FROM strokes.floats;'



df_out = pd.read_sql_query(sqlcmnd, engine)

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
for stroketime, group in df_out.groupby('rowingid'): 
    my_group_times = group['stroketime'].tolist()
    newx_out.append(my_group_times)

for distance, group in df_out.groupby('rowingid'): 
    my_group_distances = group['distance'].tolist()
    newy_out.append(my_group_distances)

listofrows = df_out['rowingid'].unique()

numlines=len(listofrows)

mypalette=Spectral11[0:numlines]

xdr = DataRange1d()
ydr = DataRange1d()


plot = Plot(
    title=None, x_range=xdr, y_range=ydr, plot_width=500, plot_height=500,
    h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)


i = 0

for lor in listofrows:
    source = ColumnDataSource(dict(x=newx_out[i], y=newy_out[i]))
    lineglyph =  Line(x="x", y="y", line_color=str(mypalette[i]), line_width=6, line_alpha=0.6)
    plot.add_glyph(source,lineglyph)
    i = i + 1






#colorlookup = zip(listofrows, mypalette_wking)

#colordf = pd.DataFrame(colorlookup,columns = ['rowingid','colorofline'])

#newdf = pd.merge(df_out, colordf, on='rowingid', how='inner')



#p.multi_line(newx, newy,
#             color=mypalette , line_width=4)

# add a text renderer to our plot (no data yet)
#r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
#           text_baseline="middle", text_align="center")

# create a callback that will add a number in a random location
#def callback():
#    newx,newy,mypalette = RefreshData()
#    source = ColumnDataSource(dict(xs=newx, ys=newx))
#    p.multi_line(x='stroketime', y='distance', source=source, color=mypalette , line_width=4)





#source = ColumnDataSource(dict(
#        stroketime=newx,
#        distance=newy,
#    )
#)




#glyph2 = MultiLine(df['stroketime'],df['distance'],source = source, line_color = df['colorofline'])

#df,newx,newy,mypalette = RefreshData()
#print df
#mysource = ColumnDataSource(df)

## this line worked
#lineglyph =  Line(x="stroketime", y="distance", line_color="#f46d43", line_width=6, line_alpha=0.6)
#plot.add_glyph(mysource, lineglyph)

#myglyph = MultiLine(xs="stroketime", ys="distance", line_color="#f46d43", line_width=6)
#plot.add_glyph(mysource, myglyph)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

curdoc().add_root(plot)

#show(plot)


# add a button widget and configure with the call back
#button = Button(label="Press Me")
#button.on_click(callback)

# put the button and plot in a layout and add to the document
#curdoc().add_root(column(button, p))
