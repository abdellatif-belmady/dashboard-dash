# import all the modules
import dash
from dash import dcc, html
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initiate the app
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP])

# Read the files
df = pd.read_csv("count.csv")
df1 = pd.read_csv("data.csv")

# Build the components
Header_component = html.H1("Traffic Analysis Dashboard", style={'color':'darken', 'text-align':'center', 'font-size':'72px'})

# Visual components

# Component1
countfig = go.FigureWidget()

countfig.add_scatter(name="bus", x = df["Time"], y = df["bus"], fill="tonexty", line_shape='spline')
countfig.add_scatter(name="car", x = df["Time"], y = df["car"], fill="tonexty", line_shape='spline')
countfig.update_layout(title="Vehicle Time Line")

# Component2
countfig_cum = go.FigureWidget()

countfig_cum.add_scatter(name="bus", x = df["Time"], y = df["bus"].cumsum(), fill="tonexty", line_shape='spline')
countfig_cum.add_scatter(name="car", x = df["Time"], y = df["car"].cumsum(), fill="tonexty", line_shape='spline')
countfig_cum.update_layout(title="Cumulative Traffic")

# Component3
indicator = go.FigureWidget(
    go.Indicator(
        mode="gauge+number",
        value=df1["car"].mean(),
        title={'text':'Speed km/h'},
    )
)
indicator.update_layout(title="Average Car Speed")

# Component4
indicator1 = go.FigureWidget(
    go.Indicator(
        mode="gauge+number",
        value=df1["bus"].mean(),
        title={'text':'Speed km/h'},
        gauge ={'bar':{'color':'cyan'}}
    )
)
indicator1.update_layout(title="Average bus Speed")

# Component5
piefig = go.FigureWidget(
    px.pie(
        labels=["car", "bus"],
        values=[df['car'].sum(), df['bus'].sum()],
        hole=0.4
    )
)

piefig.update_layout(title="Traffic Distribution")

# Design the app layout
app.layout = html.Div(
    [
        dbc.Row([
            Header_component
        ]),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=countfig)]
            ), dbc.Col(
                [dcc.Graph(figure=countfig_cum)]
            )]
        ),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=indicator)]
            ), dbc.Col(
                [dcc.Graph(figure=indicator1)]
            ), dbc.Col(
                [dcc.Graph(figure=piefig)]
            )]
        ),
    ]
)

# Run the app
app.run_server(debug=True)