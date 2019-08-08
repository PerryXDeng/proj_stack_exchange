
from bokeh.models import Panel
from bokeh.models.widgets import Div


def about_tab():

  p = Div(text="""<font size="4">
                      Interact with the Figures by Scrolling in/out and Clicking Buttons on the Right<br />
                      Predict the Context of Your Posts by Typing Them into Textbox and Clicking Predict<br />
                      <br />
                      Interactive Webapp Based on Stack Exchange Data Dump<br />
                      Contributors: Perry Deng xxd9704@rit.edu, Drew Barnes anb1852@rit.edu, Sam Snyder shs8139@rit.edu<br />
                      Our Goals, Approach, and Findings: <a href="https://www.overleaf.com/read/xnpkrdbkztrx">Overleaf</a><br />
                      Current State: Active Development for Multiclass Context Prediction, Time Series Modeling<br />
                      Source: <a href="https://github.com/PerryXDeng/stack_exchange_text_mining">Github</a><br />
                      <br />
                      Data: 11 years of Posts from English Stack Exchange Sites<br />
                      Data Source: <a href="https://archive.org/details/stackexchange">archive.org</a><br />
                      Data Size: 100 Gbs Encoded and Compressed<br />
                      Types of Analysis: Natural Language Processing, Machine Learning, Time Series<br />
                      <br />
                      Web Hosting: Nginx in Dorm Room<br />
                      Web Serving and Visualization: Bokeh over Javascript/Tornado<br />
                      Distributed Computation: PySpark over SLURM<br />
                      Cloud Database: MySQL on GCP
                  </font>
               """,
               width=1400, height=1000)


  tab = Panel(child=p, title='Usage and About')

  return tab