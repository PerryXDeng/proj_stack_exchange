from bokeh.layouts import column
from bokeh.models import Panel, WidgetBox, Legend
from bokeh.plotting import figure, show, curdoc
from bokeh import palettes
import database


def word_count_tab():
    # def make_dataset():
    #     return
    #
    # def make_plot(src):
    #     return figure()
    #
    # def update(attr, old, new):
    #     return

    # # Put controls in a single element
    # controls = WidgetBox()

    def construct_data_frame(siteId, word):
        statement = "SELECT frequency, date FROM word_frequencies WHERE siteId=" + str(siteId) + " AND word='" + word \
                    + "' AND date>='2008-09-01 00:00:00'" # + " ORDER BY date DESC"
        return database.query(statement)

    def construct_legend_name(siteId, word):
        site_name = database.get_site_name(siteId)
        return site_name + ": " + word

    def construct_data_frame_series(sites, words):
        n = len(words)
        series = [None] * n
        legends = [None] * n
        for i in range(n):
            site = sites[i]
            word = words[i]
            df = construct_data_frame(site, word)
            legend = construct_legend_name(site, word)
            series[i] = df
            legends[i] = legend
        return series, legends

    def generate_colors(n):
        # cannot have n > 20
        return palettes.Category20[n]

    def generate_plot(title, site_ids, words_list, emit_site_name=False):
        p = figure(x_axis_type="datetime", title=title, tools="wheel_zoom,reset", plot_width=1000)
        p.grid.grid_line_alpha = 0.3
        p.xaxis.axis_label = 'Month'
        p.yaxis.axis_label = 'Avg Occurrence/Post'
        series, legends  = construct_data_frame_series(site_ids, words_list)
        n = len(words_list)
        colors = generate_colors(n)
        legend_items = []
        for i in range(n):
            x = series[i]['date']
            y = series[i]['frequency']
            color = colors[i]
            line = p.line(x, y, color=color)
            squares = p.square(x, y, fill_color=None, line_color=color)
            if emit_site_name:
                legend_items.append((words_list[i], [line, squares]))
            else:
                legend_items.append((legends[i], [line, squares]))
        p.add_layout(Legend(items=legend_items, location="center"), "right")
        return p

    sites = [156, 156, 156, 156, 156, 156]
    words = ["database", "science", "mining", "sql", "hadoop", "spark"]

    sites_2 = [135, 135, 135, 135, 135]
    words_2 = ["ai", "mining", "bayesian", "svm", "neural"]

    sites_3 = [73, 73, 73, 73]
    words_3 = ["hitler", "stalin", "mao", "trump"]

    p1 = generate_plot("Select Stackoverflow Buzzwords", sites, words, emit_site_name=True)
    p2 = generate_plot("Select Stats Stack Exchange Buzzwords", sites_2, words_2, emit_site_name=True)
    p2 = generate_plot("Select History Stack Exchange Buzzwords", sites_3, words_3, emit_site_name=True)

    # Create a row layout
    layout = column(p1, p2)

    tab = Panel(child=layout, title='Buzzword Frequencies')

    return tab