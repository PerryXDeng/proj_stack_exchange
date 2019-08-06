from bokeh.layouts import row
from bokeh.models import Panel, WidgetBox
from bokeh.plotting import figure


def word_count_tab():
    def make_dataset():
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

    tab = Panel(child=layout, title='Word Count')

    return tab