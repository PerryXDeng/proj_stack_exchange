# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# database

# Each tab is drawn by one script
from scripts.classification_analysis import classification_tab
from scripts.word_count_analysis import word_count_tab
from scripts.sentiment_analysis import sentiment_tab
from scripts.post_size_analysis import post_size_tab


# Create each of the tabs
tab1 = classification_tab()
tab2 = word_count_tab()
tab3 = sentiment_tab()
tab4 = post_size_tab()

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4])

# Put the tabs in the current document for display
curdoc().add_root(tabs)