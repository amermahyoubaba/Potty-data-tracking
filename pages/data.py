from random import random
import streamlit as st
from annotated_text import annotated_text
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
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

    st.experimental_singleton.clear()
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
        current_time = now.strftime("%H:%M")
        later_time = (now + timedelta(minutes=5)).strftime("%H:%M")
        return now, current_time, later_time

    now, current_time, later_time = get_date()

    date = st.sidebar.date_input('Date:', now)
    start_time = st.sidebar.text_input("Potty start time:", current_time)
    end_time = st.sidebar.text_input("Potty end time:", later_time)

    if date.strftime("%y/%m/%d") != now.strftime("%y/%m/%d"):
        st.warning('Warning: please check if the date is accurate')

    check_time(start_time)
    check_time(end_time)

    urinate = st.sidebar.radio(
        "Urinate in toilet", ('None', 'Success', 'Accident'))
    bowel = st.sidebar.radio("Bowel movement in toilet",
                             ('None', 'Success', 'Accident'))
    mand = st.sidebar.radio("Mand", ['No', 'Independent', 'Prompted'])
    pdown = st.sidebar.radio("Pants down", ['No', 'Independent', 'Prompted'])
    pup = st.sidebar.radio("Pants up", ['No', 'Independent', 'Prompted'])
    flush = st.sidebar.radio("Flush toilet", ['No', 'Independent', 'Prompted'])

    st.markdown("#### Current Data Tracking!")

    clients = df["client"].unique()
    client_picked = st.selectbox('Pick a client', clients)
    picked_df = df[df["client"] == client_picked]

    st.markdown(
        f"Current potty interval time: **{ picked_df.iloc[-1].time_interval } minutes**!!")
    if start_time < end_time:
        st.info(f'Tracking Time Interval:  { start_time } - { end_time }')
    else:
        st.error('Error: End time must fall after start time.')

    annotated_text(
        ("Urinate in toilet", urinate),
        ("Bowel movement in toilet", bowel),
        ("Manded to go potty", mand),
        ("Pants down", pdown),
        ("Pants up", pup),
        ("Flushed toilet", flush)
    )
    st.text('\n')

    if st.button("View Client's Data"):
        st.dataframe(picked_df)

    data = {'client': client_picked, 'date': date, 'start_time': start_time,
            'end_time': end_time, 'urinate_toilet': urinate, 'bowel_movement': bowel,
            'pants_down': pdown, 'pants_up': pup, 'mand': mand, 'flush': flush,
            'time_interval': 40}

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
