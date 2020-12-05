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
class_tab = classification_tab()

buzz = Buzzwords()
buzzwords_tab = buzz.get_tab()
sent = Sentiment()
sentiment_tab = sent.get_tab()
posting = Traffic()
traffic_tab = posting.get_tab()

tab5 = about_tab()

# Put all the tabs into one application
tabs = Tabs(tabs = [traffic_tab, buzzwords_tab, sentiment_tab, class_tab, tab5])

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
curdoc().add_timeout_callback(load_data_1, 550)
