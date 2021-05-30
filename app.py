# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import csv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# ------------This is degree list----------------------------------------------
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
degrees_df = pd.DataFrame(degrees_list[1:], columns=degrees_list[0])

degrees_fig = px.bar(degrees_df, x="Undergraduate Major", y="Starting Median Salary", barmode="group")
# ----------------------This is college type-----------------------------------------------------
colleges_list1 = []
colleges_list2 = []
with open('data/salaries-by-college-type.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        colleges_list1.append(row)
        if len(colleges_list2) > 0:
            row[2] = float(row[2][1:].replace(",", ""))
            row[3] = float(row[3][1:].replace(",", ""))
        colleges_list2.append(row)
colleges_df1 = pd.DataFrame(colleges_list1[1:], columns=colleges_list1[0])
colleges_df1 = pd.DataFrame(colleges_df1["School Type"].value_counts()).reset_index()
colleges_df1.columns = ['School Type', 'Count']
colleges_fig1 = px.pie(colleges_df1, names="School Type", values="Count")
colleges_df2 = pd.DataFrame(colleges_list2[1:], columns=colleges_list2[0])
colleges_fig2 = px.scatter(colleges_df2, x="Starting Median Salary", y="Mid-Career Median Salary", color="School Type",
                           hover_name="School Name")
# ----------------------This is region------------------------------------------------
regions_list1 = []
regions_list2 = []
with open('data/salaries-by-region.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        regions_list1.append(row)
        if len(regions_list2) > 0:
            row[2] = float(row[2][1:].replace(",", ""))
            row[3] = float(row[3][1:].replace(",", ""))
        regions_list2.append(row)
regions_df1 = pd.DataFrame(regions_list1[1:], columns=regions_list1[0])
regions_df1 = pd.DataFrame(regions_df1["Region"].value_counts()).reset_index()
regions_df1.columns = ['Region', 'Count']
regions_fig1 = px.pie(regions_df1, names="Region", values="Count")
regions_df2 = pd.DataFrame(regions_list2[1:], columns=regions_list2[0])
regions_fig2 = px.scatter(regions_df2, x="Starting Median Salary", y="Mid-Career Median Salary", color="Region",
                         hover_name="School Name")

# ------------------------------------------------------------------------------------
app.layout = html.Div(children=[
    html.H1(children='College Salaries'),

    dcc.Dropdown(
        id='degree_options',
        options=[
            {'label': 'Starting Median Salary', 'value': 'Starting Median Salary'},
            {'label': 'Mid-Career Median Salary', 'value': 'Mid-Career Median Salary'},
            {'label': 'Mid-Career 10th Percentile Salary', 'value': 'Mid-Career 10th Percentile Salary'},
            {'label': 'Mid-Career 25th Percentile Salary', 'value': 'Mid-Career 25th Percentile Salary'},
            {'label': 'Mid-Career 75th Percentile Salary', 'value': 'Mid-Career 75th Percentile Salary'},
            {'label': 'Mid-Career 90th Percentile Salary', 'value': 'Mid-Career 90th Percentile Salary'},
        ],
        value='Starting Median Salary',
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
    ),

    dcc.Graph(
        id='degree_graph',
        figure=degrees_fig

    ),
    dcc.Graph
        (
        id="college_graph1",
        figure=colleges_fig1,
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
    ),
    dcc.Graph
        (
        id="college_graph2",
        figure=colleges_fig2,
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
    ),
    dcc.Graph(
        id="region_graph1",
        figure=regions_fig1,
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
    ),
    dcc.Graph(
        id="region_graph2",
        figure=regions_fig2,
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
    )
])


@app.callback(
    Output('degree_graph', 'figure'),
    Input('degree_options', 'value')
)
def update_degree(degree_options):
    new_fig = px.bar(degrees_df, x="Undergraduate Major", y=degree_options, barmode="group")
    return new_fig


if __name__ == '__main__':
    app.run_server(debug=True)
