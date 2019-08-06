from bokeh.layouts import column
from bokeh.models import Panel, Legend, Button
from bokeh.plotting import figure
import database
from scripts import helper


def sentiment_tab():
    def construct_data_frame(siteId):
        statement = "SELECT size, time FROM hourly_post_sizes WHERE siteId=" + str(siteId) + " ORDER BY time ASC"
        return database.query(statement)

    def construct_legend_name(siteId):
        site_name = database.get_site_name(siteId)
        return site_name

    def construct_data_frame_series(sites):
        n = len(sites)
        series = [None] * n
        legends = [None] * n
        for i in range(n):
            site = sites[i]
            df = construct_data_frame(site)
            legend = construct_legend_name(site)
            series[i] = df
            legends[i] = legend
        return series, legends


    def generate_plot(title, site_ids, emit_site_name=False):
        p = figure(x_axis_type="datetime", title=title, tools="wheel_zoom,reset", plot_width=1500)
        p.grid.grid_line_alpha = 0.3
        p.xaxis.axis_label = 'Time'
        p.yaxis.axis_label = 'Number of Posted Characters, Hourly'
        series, legends  = construct_data_frame_series(site_ids)
        n = len(site_ids)
        colors = helper.generate_colors(n)
        legend_items = []
        for i in range(n):
            x = series[i]['time']
            y = series[i]['size']
            color = colors[i]
            line = p.line(x, y, color=color)
            if not emit_site_name:
                legend_items.append((legends[i], [line]))
        if not emit_site_name:
            p.add_layout(Legend(items=legend_items, location="center"), "right")
        return p


    p1 = generate_plot("Hourly Sentiment Stream, Cyptocurrency Stack Exchanges", [17, 36, 57], emit_site_name=False)
    layout = column(p1)

    default_selection = [3, 17, 25, 80, 92, 93, 110, 156]
    p2 = generate_plot("Hourly Sentiment Stream, User Selected Sites", default_selection, emit_site_name=False)

    num_site_batches = 5
    check_box_groups, panel, batch_size = helper.generate_site_checkboxes(num_site_batches, default_selection)
    layout.children.append(panel)
    update_button = Button(label="Update Selection")
    layout.children.append(update_button)
    layout.children.append(p2)

    def update():
        new_sites = []
        for c in range(num_site_batches):
            col = check_box_groups[c]
            if len(col.active) > 0: # boxes checked
                new_sites.extend([c*batch_size + x + 1 for x in col.active])
        new_plot = generate_plot("Hourly Sentiment Stream, User Selected Sites", new_sites, emit_site_name=False)
        layout.children.pop()
        layout.children.append(new_plot)

    update_button.on_click(update)

    tab = Panel(child=layout, title='Sentiment Stream All Time')

    return tab