from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import *

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from dash.exceptions import PreventUpdate


card_style = {
    'width': '800px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
}


# =========  Layout  =========== #
def render_layout(username):
    template = html.Div([])
    return template 


# =========  Callbacks Page1  =========== #
@app.callback(
    Output('data-url', 'pathname',),
    Input('logout_button', 'n_clicks'),
    )
def successful(n_clicks):
    if n_clicks == None:
        raise PreventUpdate
    
    if current_user.is_authenticated:
        logout_user()
        return '/login'
    else: 
        return '/login'
