from bokeh.layouts import column
from bokeh.models import Panel, Legend
from bokeh.plotting import figure
import database
from scripts import helper


def construct_data_frame(siteId, word):
    statement = "SELECT frequency, date FROM word_frequencies WHERE siteId=" + str(siteId) + " AND word='" + word \
                + "' AND date>='2008-09-01 00:00:00' ORDER BY date ASC"
    return database.query(statement)


def construct_legend_name(siteId, word):
    site_name = database.get_site_name(siteId)
    return site_name + ": " + word


def construct_data_frame_series(site_ids, words_list):
    n = len(words_list)
    series = [None] * n
    legends = [None] * n
    for i in range(n):
        site = site_ids[i]
        word = words_list[i]
        df = construct_data_frame(site, word)
        legend = construct_legend_name(site, word)
        series[i] = df
        legends[i] = legend
    return series, legends


def generate_plot(title, site_ids, words_list, emit_site_name=False):
    p = figure(x_axis_type="datetime", title=title, plot_width=1400, tools=[])
    helper.configure_plot(p)
    p.grid.grid_line_alpha = 0.3
    p.xaxis.axis_label = 'Months'
    p.yaxis.axis_label = 'Avg Mentions Per Thousand Posts'
    series, legends = construct_data_frame_series(site_ids, words_list)
    n = len(words_list)
    colors = helper.generate_colors(n)
    legend_items = []
    for i in range(n):
        x = series[i]['date']
        y = series[i]['frequency'].values * 1000
        color = colors[i]
        line = p.line(x, y, color=color)
        squares = p.square(x, y, fill_color=None, line_color=color)
        if emit_site_name:
            legend_items.append((words_list[i], [line, squares]))
        else:
            legend_items.append((legends[i], [line, squares]))
    p.add_layout(Legend(items=legend_items, location="center"), "right")
    return p


class Buzzwords:
    def __init__(self):
        self.words_1 = ["database", "sql", "mongodb", "hadoop", "spark", "ajax", "javascript", "python", "scala", "rust"]
        self.sites_1 = [156] * len(self.words_1)
        self.words_2 = ["security", "cloud", "devops", "scalable", "workflow", "science", "blockchain", "matlab", "tensorflow", "pytorch"]
        self.sites_2 = [156] * len(self.words_2)
        self.words_5 = ["r", "java", "c"]
        self.sites_5 = [156] * len(self.words_5)
        self.words_3 = ["bayesian", "svm", "neural", "inference", "prediction", "p", "hypothesis", "bandit"]
        self.sites_3 = [135] * len(self.words_3)
        self.words_4 = ["trump", "obama", "merkel"]
        self.sites_4 = [110] * len(self.words_4)
        self.layout = column(helper.loading_plot_placeholder(), helper.loading_plot_placeholder(), helper.loading_plot_placeholder(), helper.loading_plot_placeholder(), helper.loading_plot_placeholder())

    def get_tab(self):
        return Panel(child=self.layout, title='Buzzword Frequencies All Time')

    def load_plots(self):
        p0 = generate_plot("Select StackOverflow Buzzwords", self.sites_1, self.words_1, emit_site_name=True)
        self.layout.children.pop()
        self.layout.children.insert(0, p0)
        p1 = generate_plot("Select StackOverflow Buzzwords, Continued", self.sites_2, self.words_2, emit_site_name=True)
        self.layout.children.pop()
        self.layout.children.insert(1, p1)
        p5 = generate_plot("Select StackOverflow Buzzwords, Final", self.sites_5, self.words_5, emit_site_name=True)
        self.layout.children.pop()
        self.layout.children.insert(2, p5)
        p2 = generate_plot("Select Stats Stack Exchange Buzzwords", self.sites_3, self.words_3, emit_site_name=True)
        self.layout.children.pop()
        self.layout.children.insert(3, p2)
        p3 = generate_plot("Select Politics Stack Exchange Buzzwords", self.sites_4, self.words_4, emit_site_name=True)
        self.layout.children.pop()
        self.layout.children.insert(4, p3)

    def load_handler(self, attr, old, new):
        self.load_plots()
