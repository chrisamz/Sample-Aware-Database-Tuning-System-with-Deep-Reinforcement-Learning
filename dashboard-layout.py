# dashboard_app/layout.py

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Define the layout
layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Database Tuning Dashboard"), className="mb-4")),
    
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Refresh data every second
        n_intervals=0
    ),

    dbc.Row([
        dbc.Col(dcc.Graph(id='performance-graph'), width=8),
        dbc.Col([
            html.Div(id='live-update-text'),
            dcc.Slider(
                id='action-slider',
                min=0,
                max=4,
                step=1,
                marks={i: f'Action {i}' for i in range(5)},
                value=2,
                className="mb-4"
            ),
            dbc.Button('Apply Action', id='apply-action-button', color='primary', className="mb-4", n_clicks=0)
        ], width=4),
    ]),
], fluid=True)
