from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash
from flask_login import current_user
from app import *
from pages import login, data, register
from instance import sql, convert

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# =========  Layout  =========== #
app.layout = html.Div(children=[
                dbc.Row([
                        dbc.Col([
                            #location informa qual a pagina atual
                            dcc.Location(id="base-url", refresh=False), 
                            #Store serve para saber q
                            dcc.Store(id="login-state", data=""),
                            dcc.Store(id="register-state", data=""),
                            #Div vazia para receber o layout das paginas
                            html.Div(id="page-content", style={"height": "100vh", "display": "flex", "justify-content": "center"})
                        ]),
                    ])
            ], style={"padding": "0px"},className='background')


# =========  Callbacks Page1  =========== #
    #Configuração de class para receber o usuario, com base na class flask
@login_manager.user_loader
def load_user(user_id):
    Users = user_banco_sql()
    user_row = Users.loc[Users[''] == user_id]
    if not user_row.empty:
        user = user_row.iloc[0]

        return User(username=user[''], email=user[''], password=user[''],
                    elevacao=user[''], agenda=user[''], hcc=user[''],intoper=user[''])
    return None

@app.callback(Output("base-url", "pathname"), 
            [
                Input("login-state", "data"),
                Input("register-state", "data")
            ])
def render_page_content(login_state,register_state):
    ctx = dash.callback_context
# função reservada para retornar quando o login ou register foi com sucess ou error
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigg_id == 'login-state' and login_state == "success":
            return '/data'
        if trigg_id == 'login-state' and login_state == "error":
            return '/login'
        
        
        elif trigg_id == 'register-state':

            if register_state == "":
                return '/login'
            else:
                return '/register'
    else:
        return '/'


@app.callback(Output("page-content", "children"), 
            Input("base-url", "pathname"),
            [State("login-state", "data"), State("register-state", "data")])
def render_page_content(pathname, login_state, register_state):
#Função reservada para retornar se os layout conforme a seleção do usurio com base em seu perfil
    if (pathname == "/login" or pathname == "/"):
        return login.render_layout(login_state)
    
    if pathname == "/register":
        return register.render_layout(register_state)

    if pathname == "/data":
        if current_user.is_authenticated:
            return data.render_layout(current_user.username)
        else:
            return login.render_layout(register_state)
        
    if pathname == "/elevacao":
        if current_user.is_authenticated and getattr(current_user, 'elevacao', None) == 'ADM': #Só acessa o usuario que tem permissão de ADM
            return elevacao.render_layout(current_user.username)
        else:
            return data.render_layout(login_state)

    if pathname == "/agenda":
        if current_user.is_authenticated and getattr(current_user, 'agenda', None) == 'ADM': #Só acessa o usuario que tem permissão de ADM
            return agenda.render_layout(current_user.username)
        else:
            return data.render_layout(login_state)

    if pathname == "/hcc":
        if current_user.is_authenticated and getattr(current_user, 'hcc', None) == 'ADM': #Só acessa o usuario que tem permissão de ADM
            return hcc.render_layout(current_user.username)
        else:
            return data.render_layout(login_state)

    if pathname == "/intoper":
        if current_user.is_authenticated and getattr(current_user, 'intoper', None) == 'ADM': #Só acessa o usuario que tem permissão de ADM
            return intoper.render_layout(current_user.username)
        else:
            return data.render_layout(login_state)


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)