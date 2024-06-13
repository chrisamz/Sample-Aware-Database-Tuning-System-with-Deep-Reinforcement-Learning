# dashboard_app/callbacks.py

from dash.dependencies import Input, Output, State
from .app import app
import plotly.graph_objs as go
import pandas as pd
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname='your_database',
        user='your_username',
        password='your_password',
        host='localhost',
        port=5432
    )

def fetch_data():
    conn = get_db_connection()
    query = "SELECT * FROM performance_metrics;"  # Replace with your actual performance metrics table/query
    df = pd.read_sql(query, conn)
    conn.close()
    return df

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

@app.callback(
    Output('live-update-text', 'children'),
    [Input('apply-action-button', 'n_clicks')],
    [State('action-slider', 'value')]
)
def apply_action(n_clicks, value):
    if n_clicks > 0:
        parameter_mapping = {
            0: ('work_mem', '64MB'),
            1: ('shared_buffers', '256MB'),
            2: ('max_connections', '200'),
            3: ('maintenance_work_mem', '128MB'),
            4: ('effective_cache_size', '2GB')
        }
        
        parameter, new_value = parameter_mapping[value]

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
