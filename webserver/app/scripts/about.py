
from bokeh.models import Panel
from bokeh.models.widgets import Div


def about_tab():

  p = Div(text="""
                      Interactive Webapp Based on Stack Exchange Data Dump<br />
                      <br />
                      Interact with the Figures by Clicking on the Mouse Button to the Right of the Figure<br />
                      Then Scroll in/out on X/Y Axis to Modify Domain and Range of Data Displayed<br />
                      <br />
                      Data: 11 years of Posts from English Stack Exchange Sites<br />
                      Data Source: https://archive.org/details/stackexchange<br />
                      Data Size: 100 Gbs Encoded and Compressed<br />
                      Types of Analysis: Natural Language Processing, Machine Learning, Time Series Visualization<br />
                      Current State: Active Development for More Sophisticated Statistical Analysis<br />
                      Source: https://github.com/PerryXDeng/stack_exchange_text_mining<br />
                      <br />
                      Web Hosting: Nginx in Dorm Room<br />
                      Web Serving and Visualization: Bokeh over Javascript/Tornado<br />
                      Distributed Computation Engine: PySpark over SLURM<br />
                      Cloud Database: MySQL with GCP
                      """,
                width=1000, height=1000)


  tab = Panel(child=p, title='Usage and About')

  return tab