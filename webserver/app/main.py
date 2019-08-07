# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
from scripts.classification_analysis import classification_tab
from scripts.word_count_analysis import Buzzwords
from scripts.sentiment_analysis import Sentiment
from scripts.post_size_analysis import Traffic
from scripts.about import about_tab


# Create each of the tabs
tab1 = classification_tab()

buzz = Buzzwords()
tab2 = buzz.get_tab()
sent = Sentiment()
tab3 = sent.get_tab()
posting = Traffic()
tab4 = posting.get_tab()

tab5 = about_tab()

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5])

def load_data_1():
  buzz.load_plots()
  curdoc().add_timeout_callback(load_data_2, 150)

def load_data_2():
  sent.load_plots()
  curdoc().add_timeout_callback(load_data_3, 150)

def load_data_3():
  posting.load_plots()

# Put the tabs in the current document for display
curdoc().add_root(tabs)
curdoc().add_timeout_callback(load_data_1, 250)
