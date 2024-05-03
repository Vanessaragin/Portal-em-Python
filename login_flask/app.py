import dash
import dash_bootstrap_components as dbc
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
import pyodbc
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import os
import pandas as pd
from flask_login import UserMixin

# import configparser


# config = configparser.ConfigParser()

def user_banco_sql():
    conn = pyodbc.connect(Driver='{ODBC Driver 17 for SQL Server}',
                        Server='\\',
                        Database='BANCO',
                        #Trusted_Connection='yes') QUANDO VALIDA COM O USUARIO DO WINDOWS
                        UID='SENHA',
                        PWD='LOGIN')
    #df = pd.read_sql("SELECT * FROM DWINTELIGENCIA.DBO.TB_USER_LOGIN",conn)

    cursor = conn.cursor()
    sql_query ="SELECT * FROM BANCO.DBO.TABELA"
    cursor.execute(sql_query)

    resultados = []
    for row in cursor.fetchall():
        USERNAME = row.USERNAME  # Insira o nome da coluna que você deseja armazenar na variável
        PASSWORD = row.PASSWORD
        EMAIL = row.EMAIL
        TYPE = row.TYPE
        DEP = row.DEP
        ADD = row.ADD
        DEL = row.DEL
        VIEW = row.VIEW
        USER_NAME = row.USER_NAME
        ELEVACAO = row.ELEVACAO
        AGENDA = row.AGENDA
        HCC = row.HCC      
        INTOPER = row.INTOPER   
        resultados.append((USERNAME,PASSWORD,EMAIL,TYPE,DEP,ADD,DEL,VIEW,USER_NAME,ELEVACAO,AGENDA,HCC,INTOPER))

 #   for USERNAME, PASSWORD, TYPE in resultados:
#        print(f'Coluna1: {coluna1}, Coluna2: {coluna2}')
 
    conn.commit()
    conn.close()
    df = pd.DataFrame(resultados, columns=[])
    df = pd.DataFrame(df)
    return df


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN,dbc.icons.BOOTSTRAP])
server = app.server
server.config['SECRET_KEY']='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

app.config.suppress_callback_exceptions = True


app.title = 'NAMEPAG 🌐'
app.index_string = '''
<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

class User(UserMixin):
    def __init__(self, username, email, password, elevacao, agenda, hcc,intoper):
        self.id = username  # Usando o nome de usuário como identificador único
        self.username = username
        self.email = email
        self.password = password
        self.elevacao = elevacao
        self.agenda = agenda
        self.hcc = hcc
        self.intoper = intoper

     

# Setup the LoginManager for the server
