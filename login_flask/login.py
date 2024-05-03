import os
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import *

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from dash.exceptions import PreventUpdate

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
}

# =========  Layout  =========== #
def render_layout(message):
    message = "Ocorreu algum erro durante o login." if message == "error" else message
    login = html.Div([dbc.Card([
                html.Legend("Login"),
                dbc.Input(id="user_login", placeholder="Login Azul", type="text"),
                dbc.Input(id="pwd_login", placeholder="Password", type="password"),
                dbc.Button("Login", id="login_button"),
                html.Span(message, style={"text-align": "center"}),

                html.Div([
                    html.Label("Ou", style={"margin-right": "5px"}),
                    dcc.Link("Registre-se", href="/register"),
                ], style={"padding": "20px", "justify-content": "center", "display": "flex"})

            ], style=card_style, className="align-self-center"),
                html.P([
                "Desenvolvido pela equipe da ",
                html.Span(
                    "Inteligência Operacional",
                    id="tooltip-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                ),],style={'color':'white','font-size':'10px',"justify-content": "center"}),
        dbc.Tooltip(
            "inteligenciaoperacional@voeazul.com.br",
            target="tooltip-target",
        ),
                
                ],className="align-self-center")
    return login


# =========  Callbacks Page1  =========== #
@app.callback(
    Output('login-state', 'data'),
    Input('login_button', 'n_clicks'), 
    [State('user_login', 'value'), 
     State('pwd_login', 'value')],
)
def successful(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate
    
    Users = user_banco_sql()
    user_data = Users.loc[Users['USERNAME'] == username]
    
    if user_data.empty:
        print("Usuário não encontrado.")
        return "error"
    
    user_data = user_data.iloc[0]
    hashed_password = user_data['PASSWORD']
    
    if hashed_password and password:
        if check_password_hash(hashed_password, password):
            user = User(username=user_data[''], email=user_data[''], password=hashed_password,
                        elevacao=user_data[''], agenda=user_data[''], hcc=user_data[''],intoper=user_data['']
                        )
            login_user(user)
            print("success")
            return "success"
        else:
            print("Senha incorreta.")
            return "error"
    else:
        print("Erro: dados de usuário incompletos.")
        return "error"
