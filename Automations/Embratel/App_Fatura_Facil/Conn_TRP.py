from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


def get_login(id_cliente):
    server = 'mg8.database.windows.net'
    porta = '1433'
    username = 'mg8-rafael'
    password = quote_plus('Chvmyoz1gd24')
    database = 'TRP'
    params = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:' + server + ',' + porta + ';DATABASE=' + \
        database + ';UID=' + username + ';PWD=' + password + \
        ';Connection Timeout=120;TrustServerCertificate=yes'
    conn = f'mssql+pyodbc:///?odbc_connect={params}'

    con = create_engine(conn)
    con = con.connect()

    cliente = con.execute(text(
        f'select nome_cliente from dbo.clientes where id_cliente = {id_cliente}')).fetchone()
    cliente = list(cliente)[0]

    cnpj = con.execute(text(
        f'select cnpj from dbo.contratos where id_cliente = {id_cliente} and id_operadora = 11')).fetchone()
    cnpj = list(cnpj)[0]
    if str(id_cliente) == '40':
        cnpj = '0' + str(cnpj)

    dados_login = con.execute(text(
        f'select * from dbo.faturas_grupo where id_cliente = {id_cliente} and id_operadora = 11')).fetchone()
    dados_login = list(dados_login)
    login = dados_login[2]
    senha = dados_login[3]

    con.close()
    return login, senha, cnpj, cliente
