from bokeh.layouts import column
from bokeh.models import Panel, Legend, Button
from bokeh.plotting import figure
import database
from scripts import helper
import numpy as np


def sentiment_tab():
    def construct_data_frame(siteId):
        statement = "SELECT value, date FROM sentiment_values_hourly WHERE siteId=" + str(siteId) + " ORDER BY date ASC"
        return database.query(statement)

    def construct_legend_name(siteId):
        site_name = database.get_site_name(siteId)
        return site_name

    def construct_data_frame_series(sites, sliding_window=0):
        n = len(sites)
        series = [None] * n
        legends = [None] * n
        for i in range(n):
            site = sites[i]
            df = construct_data_frame(site)
            legend = construct_legend_name(site)
            if sliding_window > 1:
                df['value'] = np.convolve(df['value'].values, np.ones(sliding_window), 'same')/float(sliding_window)
            series[i] = df
            legends[i] = legend
        return series, legends


    def generate_plot(title, site_ids, emit_site_name=False, sliding_window=0):
        p = figure(x_axis_type="datetime", title=title, tools="wheel_zoom,reset", plot_width=1500)
        p.grid.grid_line_alpha = 0.3
        p.xaxis.axis_label = 'Time'
        p.yaxis.axis_label = 'Average Sentiment, Hourly'
        series, legends  = construct_data_frame_series(site_ids, sliding_window)
        n = len(site_ids)
        colors = helper.generate_colors(n)
        legend_items = []
        for i in range(n):
            x = series[i]['date']
            y = series[i]['value']
            color = colors[i]
            line = p.line(x, y, color=color)
            if not emit_site_name:
                legend_items.append((legends[i], [line]))
        if not emit_site_name:
            p.add_layout(Legend(items=legend_items, location="center"), "right")
        return p


    p1 = generate_plot("Hourly Sentiment Stream (Daily Moving Average), Cyptocurrency Stack Exchanges", [17, 36, 57],
                       emit_site_name=False, sliding_window=24)
    layout = column(p1)

    default_selection = [3, 25, 80, 92, 93, 110]
    p2 = generate_plot("Hourly Sentiment Streams (Daily Moving Average), User Selected Sites", default_selection,
                        emit_site_name=False, sliding_window=24)
    p3 = generate_plot("Hourly Sentiment Streams, User Selected Sites", default_selection,
                        emit_site_name=False, sliding_window=0)
    num_site_batches = 5
    check_box_groups, panel, batch_size = helper.generate_site_checkboxes(num_site_batches, default_selection)
    layout.children.append(panel)
    update_button = Button(label="Update Selection (No More than 20)")
    layout.children.append(update_button)
    layout.children.append(p2)
    layout.children.append(p3)

    def update():
        new_sites = []
        for c in range(num_site_batches):
            col = check_box_groups[c]
            if len(col.active) > 0: # boxes checked
                new_sites.extend([c*batch_size + x + 1 for x in col.active])
        new_moving_average = generate_plot("Hourly Sentiment Streams (Daily Moving Average), User Selected Sites",
                                            new_sites, emit_site_name=False, sliding_window=24)
        new_normie = generate_plot("Hourly Sentiment Streams, User Selected Sites",
                                    new_sites, emit_site_name=False, sliding_window=0)
        layout.children.pop()
        layout.children.pop()
        layout.children.append(new_moving_average)
        layout.children.append(new_normie)

    update_button.on_click(update)

    tab = Panel(child=layout, title='Sentiment Stream All Time')

    return tab