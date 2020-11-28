# myapp.py

from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

# create a plot and style its properties
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

# add a text renderer to our plot (no data yet, data created on client javascript callback)
renderer = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
                  text_baseline="middle", text_align="center")

rendered_data = renderer.data_source

# for new colors on update
i = 0

# create a callback that will add a number in a random location, triggered by button to be added later
def callback():
    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = rendered_data.data['x'] + [random() * 70 + 15]
    new_data['y'] = rendered_data.data['y'] + [random() * 70 + 15]
    new_data['text_color'] = rendered_data.data['text_color'] + [RdYlBu3[i % 3]]
    new_data['text'] = rendered_data.data['text'] + [str(i)]
    rendered_data.data = new_data

    i = i + 1

# add a button widget and configure its click event with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))