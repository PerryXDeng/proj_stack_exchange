from bokeh.layouts import row
from bokeh.models import Panel, WidgetBox
from bokeh.plotting import figure


def classification_tab():

    def make_dataset(): # need to add dat input hereish
        pass

    def make_plot(src):
        return figure()

    def update(attr, old, new):
        pass

    p = make_plot(make_dataset())

    # Put controls in a single element
    controls = WidgetBox()

    # Create a row layout
    layout = row(controls, p)

    tab = Panel(child=layout, title='Classification')

    return tab