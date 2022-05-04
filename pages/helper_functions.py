import pandas as pd
import plotly.express as px


def pie_chart(df, column):
    data = {}
    for col, row in df.iterrows():
        x = row[column]
        if x in data.keys():
            data[x] += 1
        else:
            data[x] = 1
    pie = pd.DataFrame(data, index=['Value']).T

    pie_chart = px.pie(pie, values='Value',
                       names=pie.index, title=f"{ column } chart",
                       hole=.3)
    return pie_chart


def clean_data(df):
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    df.index = pd.to_datetime(df['date'])
    df.drop(columns=['date'], inplace=True)

    return df
