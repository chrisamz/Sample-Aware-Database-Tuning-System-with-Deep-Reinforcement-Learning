# dashboard_app/app.py

import dash
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Database Tuning Dashboard"
server = app.server
