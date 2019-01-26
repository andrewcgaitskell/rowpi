
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import random

p = figure(plot_width=400, plot_height=400)
r1 = p.line([], [], color="firebrick", line_width=2)
r2 = p.line([], [], color="navy", line_width=2)

ds1 = r1.data_source
ds2 = r2.data_source

@linear()
def update(step):
    ds1.data['x'].append(step)
    ds1.data['y'].append(random.randint(0,100))
    ds2.data['x'].append(step)
    ds2.data['y'].append(random.randint(0,100))  
    ds1.trigger('data', ds1.data, ds1.data)
    ds2.trigger('data', ds2.data, ds2.data)

curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 500)
