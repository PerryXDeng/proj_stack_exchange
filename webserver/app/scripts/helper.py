from bokeh import palettes
from bokeh.models.widgets import CheckboxGroup, Div
from bokeh.models import WheelZoomTool, SaveTool, ResetTool, Title
from bokeh.layouts import row
import database


def generate_colors(n):
  # cannot have n > 20
  if n < 3:
    n = 3
  if n < 11:
    return palettes.Category10[n]
  return palettes.Category20[n]


def generate_site_checkboxes(num_site_batches, default_selection):
  sites = database.get_all_site_names_sorted_by_site_id()
  total = len(sites)
  batch_size = total // num_site_batches
  check_box_groups = []
  panel = None
  for i in range(num_site_batches):
    end = ((i + 1) * batch_size if i * batch_size < total else total)
    check_box_column = CheckboxGroup(labels=sites[i * batch_size:end],
                                     active=[x - 1 - i * batch_size for x in default_selection if
                                             i * batch_size < x < (i + 1) * batch_size])
    check_box_groups.append(check_box_column)
    if panel is None:
      panel = row(check_box_column)
    else:
      panel.children.append(check_box_column)
  return check_box_groups, panel, batch_size


def loading_plot_placeholder():
  return Div(text='<p style="font-size:50px;">⏳⌛Crunching Numbers, Please Wait⌛⏳</p>', height=500, width=1400)


def configure_plot(plot):
  tools = [WheelZoomTool(dimensions = "width"), WheelZoomTool(dimensions = "height"),
           SaveTool(), ResetTool()]
  for tool in tools: plot.add_tools(tool)
  plot.toolbar.active_scroll = tools[0]
  plot.add_layout(Title(
    text="interactively view the data at https://pdeng.student.rit.edu                                                                             data source: archive.org/details/stackexchange",
    align="right"), "below")
