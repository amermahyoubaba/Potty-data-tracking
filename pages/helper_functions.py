import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def set_df(df, column):
    data = {}
    for col, row in df.iterrows():
        x = row[column]
        if x in data.keys():
            data[x] += 1
        else:
            data[x] = 1

    table = pd.DataFrame(data, index=['Value']).T
    return table


def success_streak(df, tracked):
    map = {'None': 0, 'Success': 1, 'Accident': -1}

    value = map[tracked]
    prev_streak = df.tail(1)['success_streak'].values[0]

    if value == 0:
        return prev_streak

    elif value == 1:
        if prev_streak >= 0:
            streak = prev_streak + 1

        elif prev_streak < 0:
            streak = 0

    elif value == -1:
        if prev_streak <= 0:
            streak = prev_streak - 1
        elif prev_streak > 0:
            streak = 0

    return streak


def time_interval(df, streak):
    prev_interval = df.tail(1)['time_interval'].values[0]

    if streak == 3:
        current_interval = prev_interval + 5

    elif streak == -3:
        current_interval = prev_interval - 5

    else:
        current_interval = prev_interval

    return current_interval


def pie_chart(df, column1, column2):

    pie1 = set_df(df, column1)
    pie2 = set_df(df, column2)

    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, specs=[
                        [{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(values=pie1.Value, labels=pie1.index, title=column1),
                  1, 1)
    fig.add_trace(go.Pie(values=pie2.Value, labels=pie2.index, title=column2),
                  1, 2)
    fig.update_traces(hole=.4, textinfo="label+percent+text+value")

    fig.update_layout(
        template='seaborn',
        autosize=True,
        # width=600,
        height=250,
        margin=dict(l=0, r=0, b=0, t=0, pad=0))
    # title_text="Global Emissions 1990-2011")
    # Add annotations in the center of the donut pies.
    # annotations=[dict(text=column1, x=0.18, y=0.5, font_size=20, showarrow=False),
    #  dict(text=column2, x=0.82, y=0.5, font_size=20, showarrow=False)])

    return fig


def bar_chart1(df):
    fig = px.bar(df[['urinate_toilet', 'bowel_movement']].melt(
    ), x='variable', color='value', barmode='group', template='seaborn')
    return fig


def bar_chart2(df):
    fig = px.bar(df[['mand', 'pants_down', 'pants_up', 'flush']].melt(
    ), x='variable', color='value', barmode='group', template='seaborn')
    return fig


def clean_data(df):
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    df.index = pd.to_datetime(df['date'])
    df.drop(columns=['date'], inplace=True)

    return df


def color_map(word):
    colors = {'None': '#F08080', 'Success': '#8FBC8F',
              'Accident': '#DDA0DD', 'Independent': '#90EE90', 'Prompted': '#AFEEEE'}
    return colors[word]
