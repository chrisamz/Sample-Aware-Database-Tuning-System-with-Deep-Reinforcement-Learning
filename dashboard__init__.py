# dashboard/__init__.py

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import psycopg2
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Database Tuning Dashboard"

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname='your_database',
        user='your_username',
        password='your_password',
        host='localhost',
        port=5432
    )

# Fetch data from the database
def fetch_data():
    conn = get_db_connection()
    query = "SELECT * FROM performance_metrics;"  # Replace with your actual performance metrics table/query
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Database Tuning Dashboard'),

    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Refresh data every second
        n_intervals=0
    ),

    dcc.Graph(
        id='performance-graph'
    ),

    html.Div(id='live-update-text'),

    dcc.Slider(
        id='action-slider',
        min=0,
        max=4,
        step=1,
        marks={i: f'Action {i}' for i in range(5)},
        value=2,
    ),
    
    html.Button('Apply Action', id='apply-action-button', n_clicks=0)
])

# Update performance graph callback
@app.callback(
    Output('performance-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = fetch_data()
    traces = [
        go.Scatter(
            x=df['timestamp'],
            y=df['metric_value'],
            mode='lines+markers',
            name='Performance Metric'
        )
    ]
    return {
        'data': traces,
        'layout': go.Layout(
            title='Database Performance Over Time',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Performance Metric'},
            hovermode='closest'
        )
    }

# Apply action button callback
@app.callback(
    Output('live-update-text', 'children'),
    [Input('apply-action-button', 'n_clicks')],
    [dash.dependencies.State('action-slider', 'value')]
)
def apply_action(n_clicks, value):
    if n_clicks > 0:
        # Mapping of action index to parameter names and values
        parameter_mapping = {
            0: ('work_mem', '64MB'),
            1: ('shared_buffers', '256MB'),
            2: ('max_connections', '200'),
            3: ('maintenance_work_mem', '128MB'),
            4: ('effective_cache_size', '2GB')
        }
        
        parameter, new_value = parameter_mapping[value]

        # Adjust parameter using backend's ParameterAdjuster
        from backend.parameter_adjuster import ParameterAdjuster
        db_config = {
            'dbname': 'your_database',
            'user': 'your_username',
            'password': 'your_password',
            'host': 'localhost',
            'port': 5432
        }
        adjuster = ParameterAdjuster(db_config)
        adjuster.adjust_parameter(parameter, new_value)
        adjuster.reload_configuration()
        adjuster.close()

        return f'Applied action: Set {parameter} to {new_value}'
    return 'Select an action to apply.'

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
