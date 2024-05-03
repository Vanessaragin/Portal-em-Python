from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from werkzeug.security import generate_password_hash
from dash.exceptions import PreventUpdate

from app import *

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
}



# =========  Layout  =========== #
def render_layout(message):
    message = "Ocorreu algum erro durante o registro." if message == "error" else message

    layout = dbc.Card([
                html.Legend("Registrar"),
                dbc.Input(id="user_register", placeholder="Nome Completo", type="text"),
                dbc.Input(id="re_register", placeholder="RE", type="text"),
                dbc.Input(id="pwd_register", placeholder="Password", type="password",autoComplete='new-password'),
                dbc.Input(id="email_register", placeholder="E-mail", type="email"),
                dbc.Button("Registrar", id='register-button'),
                html.Span(message, style={"text-align": "center"}),

                html.Div([
                    html.Label("Ou ", style={"margin-right": "5px"}),
                    dcc.Link("faça login", href="/login"),
                ], style={"padding": "20px", "justify-content": "center", "display": "flex",'margin-bottom':'0px'}),
                html.Div([html.I(className="bi bi-info-circle-fill me-2"),
                    html.Label("Após realizar o cadastro, o usuário deve enviar um email para 'inteligencia.operacional@voeazul.com.br' solicitando a aprovação e informando o tipo de usuário desejado.", 
                               style={"margin-right": "5px",'font-size':'8px',"margin-top": "0px",}),

                ], style={"padding": "20px", "justify-content": "center", "display": "flex"})

            ], style=card_style, className="align-self-center")
    return layout



# =========  Callbacks Page1  =========== #
@app.callback(
    Output('register-state', 'data'),
    Input('register-button', 'n_clicks'), 
    [State('user_register', 'value'), 
     State('re_register', 'value'), 
    State('pwd_register', 'value'),
    State('email_register', 'value')],
)
def successful(n_clicks, username, re, password, email):

    print(username,re,password,email)
    if n_clicks == None:
        raise PreventUpdate

    if username is not None and password is not None and email is not None and re is not None:
        hashed_password = generate_password_hash(password, method='sha256')

        usuario_logado = email.split('@')[0]

        # Conectar ao banco de dados SQL Server
        conn = pyodbc.connect(
            Driver='{ODBC Driver 17 for SQL Server}',
            Server='',
            Database='BANCO',
            UID='SENHA',
            PWD='LOGIN'
        )

        cursor = conn.cursor()

        # Define a query SQL para inserção
        sql_insert = """
        INSERT INTO BANCO.APP.TABELA (
        VALUES (?, ?, ?, ?,?)
        """

        try:
            # Executa a operação de inserção
            cursor.execute(sql_insert,usuario_logado, username, hashed_password, email, re)
            
            # Confirma a transação
            conn.commit()
            print("Usuário inserido com sucesso!")
            return ''
        except Exception as e:
            # Se ocorrer algum erro, desfaz as alterações
            conn.rollback()
            print("Erro ao inserir usuário:", e)
            return 'error'
        finally:
            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()
    else:
        return 'error'