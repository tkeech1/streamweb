import streamlit as st
import datetime
import pytz
from utils.metrics import log_runtime
import streamlit.components.v1 as components

short_title = "Energy Data Visualization"
long_title = "Energy Data Visualization with Altair & Tableau"
key = 8
content_date = datetime.datetime(2023, 5, 19).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    #location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    location.markdown("""I recently created a data visualization project using Tableau and Altair as part of the Cal Berkeley Master 
    in Data Science (MIDS) program. I really like Altair's "grammer of graphics" approach which was taken from ggplot and others. I find
    it much more intuitive to create visualizations than matplotlib. Altair also has an awesome gallery of [examples](https://altair-viz.github.io/gallery/index.html).     
    """)    

    location.markdown("""Tableau is always interesting to work with. I've used it at work to create dashboards but I've always found the UI
    to be a little slower than I would prefer. Tableau makes it very easy to add interactivity (facets, filters, tooltips, etc.) and publish 
    your work to the web through Tableau Public. 
    """)    

    location.markdown("""
[W209 Data Visualization Project](http://w209project.s3-website-us-east-1.amazonaws.com/index.html)
    """)    





