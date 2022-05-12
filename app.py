import streamlit as st

# Custom imports
from multipage import MultiPage
# import your pages here
from pages import data, visualization
# Create an instance of the app
app = MultiPage()

# Title of the main page
# st.title("Potty Data Tracker")

# Add all your applications (pages) here
app.add_page("Track Data", data.app)
# app.add_page("Data table", visualization.app)
app.add_page("Data Vizualization", visualization.app)

# The main app
app.run()
