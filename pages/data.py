from random import random
import streamlit as st
from annotated_text import annotated_text
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from pages.helper_functions import color_map, success_streak, time_interval
from htbuilder import div, styles, classes, fonts
import time
import random
# from PIL import Image
import os
import re


def app():

    # st.image(
    #     image,
    #     width=100,
    # )

    r = re.compile('\d{2}:\d{2}')

    def check_time(time):
        if (len(time) == 5) & (r.match(time) is not None):
            pass
        else:
            st.error(
                'Error: Please enter a valid 24h time format, ex: 08:00, 13:05')

    st.title("Potty Data Tracker!!")
    # st.sidebar.title("About")
    st.sidebar.info(
        "Enter Potty tracking data below:")

    # st.sidebar.slider(
    #     "Potty time range:",
    #     value=(time(8, 30), time(12, 45)))

    df = pd.read_csv('test_data.csv').drop(columns=['Unnamed: 0'])
    # df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

    @st.experimental_singleton
    def get_date():
        now = dt.now()
        prev_time = (now - timedelta(minutes=5)).strftime("%H:%M")
        current_time = now.strftime("%H:%M")
        return now, prev_time, current_time

    now, prev_time, current_time = get_date()

    date = st.sidebar.date_input('Date:', now)
    start_time = st.sidebar.text_input("Potty start time:", prev_time)
    end_time = st.sidebar.text_input("Potty end time:", current_time)

    if date.strftime("%y/%m/%d") != now.strftime("%y/%m/%d"):
        st.warning('Warning: please check if the date is accurate')

    check_time(start_time)
    check_time(end_time)

    urinate = st.sidebar.radio(
        "Urinate in toilet", ('None', 'Success', 'Accident'))
    bowel = st.sidebar.radio("Bowel movement in toilet",
                             ('None', 'Success', 'Accident'))
    mand = st.sidebar.radio("Mand", ['None', 'Independent', 'Prompted'])
    pdown = st.sidebar.radio("Pants down", ['None', 'Independent', 'Prompted'])
    pup = st.sidebar.radio("Pants up", ['None', 'Independent', 'Prompted'])
    flush = st.sidebar.radio(
        "Flush toilet", ['None', 'Independent', 'Prompted'])

    st.markdown("#### Current Data Tracking!")

    clients = df["client"].unique()
    client_picked = st.selectbox('Pick a client', clients)
    picked_df = df[df["client"] == client_picked]

    st.info(
        f"""Current potty interval time: **{ picked_df.iloc[-1].time_interval } minutes**!
         Potty success streak: **{ picked_df.iloc[-1].success_streak }**!
        \n Tracking for client: **{client_picked}**""")

    metric1, metric2 = st.columns(2)

    interval_diff = picked_df.iloc[-1].time_interval - \
        picked_df.iloc[-2].time_interval
    metric1.metric(
        "Current Time Interval", picked_df.iloc[-1].time_interval, int(interval_diff))

    metric2.metric(
        "Current Success Streak", picked_df.iloc[-1].success_streak, int(picked_df.iloc[-2].success_streak))

    if start_time < end_time:
        st.info(f'Tracking Time Interval:  { start_time } - { end_time }')
    else:
        st.error('Error: End time must fall after start time.')

    annotated_text(
        ("Urinate in toilet", urinate, color_map(urinate)),
        ("Bowel movement in toilet", bowel, color_map(bowel)),
        ("Manded to go potty", mand, color_map(mand)),
        ("Pants down", pdown, color_map(pdown)),
        ("Pants up", pup, color_map(pup)),
        ("Flushed toilet", flush, color_map(flush)),
    )
    st.text('\n')

    col1, col2, col3 = st.columns(3)

    if col1.button("View Client's Data"):
        st.dataframe(picked_df)

    if col2.button("Clear Cache!"):
        st.experimental_singleton.clear()

    col3.download_button(
        label="Download data as CSV",
        data=picked_df.to_csv(),
        file_name=f'{client_picked}_potty_data.csv',
        mime='text/csv',
    )

    streak = success_streak(picked_df, bowel)
    interval = time_interval(picked_df, streak)

    data = {'client': client_picked, 'date': date, 'start_time': start_time,
            'end_time': end_time, 'urinate_toilet': urinate, 'bowel_movement': bowel,
            'pants_down': pdown, 'pants_up': pup, 'mand': mand, 'flush': flush,
            'time_interval': interval, 'success_streak': streak}

    if st.sidebar.button("Track"):

        with st.spinner('Wait for it...'):
            try:
                df = df.append(data, ignore_index=True)
                df.to_csv('test_data.csv')
                # Clears all singleton caches:
                st.experimental_singleton.clear()
                st.success('Successfully tracked data! Thank you!!')
                st.balloons()

            except:
                st.error(
                    'Error: There was an error tracking your data!! \n Please verify the data inputted and refresh the page!')
