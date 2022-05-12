import streamlit as st
import pandas as pd
from datetime import datetime as dt
import datetime
from dateutil.relativedelta import relativedelta
from pages.helper_functions import *


def app():

    st.title('Potty Data Graphs!!')

    df = pd.read_csv('test_data.csv')
    df = clean_data(df)

    # today = datetime.date.today()
    # tomorrow = today + datetime.timedelta(days=1)
    start_day = dt.today() - relativedelta(day=1)
    last_day = dt.today() + relativedelta(day=31)

    try:
        start_date, end_date = st.sidebar.date_input(
            'Start date  - End date :', value=[start_day, last_day])
    except:
        st.error(
            'Please enter a valid date range \n\n Ensure you have selected a start date and an end date')

    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date: `%s`' %
                   (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')

    clients = df["client"].unique()
    client_picked = st.selectbox('Pick a client', clients)
    picked_df = df[df["client"] == client_picked]

    type_chart = st.sidebar.selectbox('Pick a chart type', [
        'Pie Chart', 'Bar Chart'])
    st.markdown(f'### { type_chart }')

    # column = st.selectbox('Pick a column to graph', [
    #                       'urinate_toilet', 'bowel_movement'])
    if type_chart == 'Pie Chart':
        chart1 = pie_chart(picked_df, 'urinate_toilet', 'bowel_movement')
        st.plotly_chart(chart1, use_container_width=True)
        st.write('\n')

        chart2 = pie_chart(picked_df, 'pants_down', 'pants_up')
        st.plotly_chart(chart2, use_container_width=True)
        st.write('\n')

        chart3 = pie_chart(picked_df, 'mand', 'flush')
        st.plotly_chart(chart3, use_container_width=True)

    if type_chart == 'Bar Chart':
        chart1 = bar_chart1(picked_df)
        st.plotly_chart(chart1, use_container_width=True)
        st.write('\n')

        chart2 = bar_chart2(picked_df)
        st.plotly_chart(chart2, use_container_width=True)

    # st.line_chart(picked_df[['time_interval']])
