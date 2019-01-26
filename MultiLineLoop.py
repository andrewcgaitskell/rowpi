from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.palettes import Category10
from bokeh.plotting import figure

p2 = figure(plot_width=600, plot_height=300)
grp_list = df.group.unique()
for i in range(len(grp_list)):
     source = ColumnDataSource(
     data={'x':df.loc[df.group == grp_list[i]].x,
           'group':df.loc[df.group == grp_list[i]].group,
           'y':df.loc[df.group == grp_list[i]].y})
p2.line(x='x',
        y='y',
        source=source,
        legend = grp_list[i],
        color = (Category10[3])[i])
#add tool tips
hover = HoverTool(tooltips =[
     ('group','@group'),('x','@x'),('y','@y')])
p2.add_tools(hover)
show(p2)
