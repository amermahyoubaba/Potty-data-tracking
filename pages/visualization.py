import streamlit as st
import pandas as pd
from datetime import datetime as dt
import datetime
from pages.helper_functions import pie_chart, clean_data


def app():

    st.title('Potty Data Graphs!!')

    df = pd.read_csv('test_data.csv')
    df = clean_data(df)

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    start_date, end_date = st.sidebar.date_input(
        'start date  - end date :', [])

    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' %
                   (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')

    clients = df["client"].unique()
    client_picked = st.selectbox('Pick a client', clients)
    picked_df = df[df["client"] == client_picked]

    column = st.selectbox('Pick a column to graph', [
                          'urinate_toilet', 'bowel_movement'])
    chart1 = pie_chart(picked_df, column)
    st.plotly_chart(chart1)

    column2 = st.selectbox('Pick a column to graph', [
        'mand', 'pants_up', 'pants_down', 'flush'])
    chart2 = pie_chart(picked_df, column2)

    st.plotly_chart(chart2)

    # st.line_chart(picked_df[['time_interval']])
