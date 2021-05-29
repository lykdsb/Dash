# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import csv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
degrees_list = []
with open('data/degrees-that-pay-back.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(degrees_list) > 0:
            row[1] = float(row[1][1:].replace(",", ""))
            row[2] = float(row[2][1:].replace(",", ""))
            row[4] = float(row[4][1:].replace(",", ""))
            row[5] = float(row[5][1:].replace(",", ""))
            row[6] = float(row[6][1:].replace(",", ""))
            row[7] = float(row[7][1:].replace(",", ""))
        degrees_list.append(row)
df = pd.DataFrame(degrees_list[1:], columns=degrees_list[0])

fig = px.bar(df, x="Undergraduate Major", y="Starting Median Salary", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello World'),

    dcc.Dropdown(
        options=[
            {'label': 'Starting Median Salary', 'value': 'SMS'},
            {'label': 'Mid-Career Median Salary', 'value': 'MCMS'},
            {'label': 'Mid-Career 10th Percentile Salary', 'value': 'MC10'},
            {'label': 'Mid-Career 25th Percentile Salary', 'value': 'MC25'},
            {'label': 'Mid-Career 75th Percentile Salary', 'value': 'MC75'},
            {'label': 'Mid-Career 90th Percentile Salary', 'value': 'MC90'},
        ],
        value='MTL'
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
