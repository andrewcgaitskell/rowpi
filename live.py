import time
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show

# prepare output to server
output_server("animated_line")

p = figure(plot_width=400, plot_height=400)
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], name='ex_line')
show(p)

# create some simple animation..
# first get our figure example data source
renderer = p.select(dict(name="ex_line"))
ds = renderer[0].data_source

while True:
    # Update y data of the source object
    shuffle(ds.data["y"])

    # store the updated source on the server
    cursession().store_objects(ds)
    time.sleep(0.5)
