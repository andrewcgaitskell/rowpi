######## bokeh serve --show RowViz2.py


from bokeh.layouts import column

from bokeh.models import Plot

from bokeh.models import Grid
from bokeh.models import DataRange1d
from bokeh.models import ColumnDataSource

from bokeh.palettes import Spectral11
from bokeh.plotting import figure, curdoc
from bokeh.server.server import Server
from bokeh.themes import Theme

from bokeh.models.glyphs import Line
from bokeh.io import curdoc, show
from bokeh.plotting import reset_output

from sqlalchemy import create_engine

import pandas as pd

engine = create_engine('postgresql://pi:raspberry@localhost:5432/rowingdata')

#sqlcmnd = 'SELECT stroketime, distance, spm, power, pace, calhr, calories, heartrate, status, rowingid FROM strokes.floats;'

# sqlcmnd = 'SELECT stroketime, distance,rowingid FROM data.strokes;'

sqlcmnd = 'select row_number() OVER(PARTITION BY rowingid ORDER BY distance) strokecounter, stroketime, distance,pace,  rowingid FROM data.strokes;'

df_out = pd.read_sql_query(sqlcmnd, engine)

newx_out = []
newy_out = []

listofrows_out = df_out['rowingid'].unique()

numlines=len(listofrows_out)

mypalette_out=Spectral11[0:numlines]

xdr = DataRange1d()
ydr = DataRange1d()

######## bokeh - multi_line #############
grp_list = df_out['rowingid'].unique()

rowscount = len(grp_list)

simplelegend = []

for r in range(0,rowscount):
    simplelegend.append(r)


xs = [df_out.loc[df_out['rowingid'] == i].strokecounter for i in grp_list]
print("xs",xs)


ys = [df_out.loc[df_out['rowingid'] == i].pace for i in grp_list]
source = ColumnDataSource(data=dict(
     x = xs,
     y = ys,
     color = mypalette_out,
     group = simplelegend))
p3 = figure(plot_width=1000, plot_height=600)
p3.multi_line(
     xs='x',
     ys='y',
     legend='group',
     source=source,
     line_color='color')

def update():
    
    df_out = pd.read_sql_query(sqlcmnd, engine)

    newx_out = []
    newy_out = []

    listofrows_out = df_out['rowingid'].unique()

    numlines=len(listofrows_out)

    mypalette_out=Spectral11[0:numlines]

    xdr = DataRange1d()
    ydr = DataRange1d()

    ######## bokeh - multi_line #############
    grp_list = df_out['rowingid'].unique()

    rowscount = len(grp_list)

    simplelegend = []

    for r in range(0,rowscount):
        simplelegend.append(r)

    xs = [df_out.loc[df_out['rowingid'] == i].strokecounter for i in grp_list]

    ys = [df_out.loc[df_out['rowingid'] == i].pace for i in grp_list]
    
    source = ColumnDataSource(data=dict(
         x = xs,
         y = ys,
         color = mypalette_out,
         group = simplelegend))
    
    p3.source = source
    
curdoc().add_root(p3)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 200)
