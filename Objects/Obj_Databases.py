import os
import sqlite3
from os.path import dirname, join
from typing import List, Tuple

import pandas as pd


class ControlDatabases:
    def __init__(self, database: str, database_path: str = None) -> None:
        """
        Classe que controla os bancos de dados selecionados.

        Args:
            database (str): Insira o nome do banco de dados desejado.
            database_path (str, optional): Insira o caminho completo até o banco de dados desejado.
        """
        if not database_path:
            main_path = dirname(__file__)

            i = 0
            while 'Databases' not in os.listdir(main_path):
                main_path = dirname(main_path)

                i += 1
                if i == 5:
                    raise ('pasta não encontrada')

            database_path = join(main_path, 'Databases')

        self.__database__ = join(database_path, database)
        self.__con__ = None

    def __exit__(self) -> None:
        """Fecha a conexão com o banco de dados ao encerrar a aplicação."""
        self.disconnect()

    def __get_table_info__(self, table_name: str) -> dict:
        """
        Obtém as informações da tabela.
        """
        con = self.connect()
        cur = con.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = cur.fetchall()
        return {c[1]: c[2] for c in columns}

    def connect(self) -> sqlite3.Connection:
        """
        Estabelece uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: A conexão estabelecida com o banco de dados.
        """
        self.__con__ = sqlite3.connect(self.__database__)
        return self.__con__

    def disconnect(self) -> None:
        """Fecha a conexão com o banco de dados."""
        if self.__con__:
            self.__con__.close()

    def command(self, command: str, return_df: bool = True, **kwargs):
        """
        Manda um comando ao banco de dados.

        Args:
            command (str): Comando a ser enviado.
            return_df (bool, optional): Retorna a query em formato de DataFrame pandas. Defaults to True.

        Returns:
            pd.DataFrame or list: Resultado da consulta, em formato DataFrame pandas se return_df for True, senão em uma lista.
        """
        con = self.connect()
        if return_df:
            df = pd.read_sql(command, con, **kwargs)
            return df
        else:
            cur = con.cursor()
            res = cur.execute(command, **kwargs)
            return res.fetchall()

    def create_table(self, table_name: str, columns: dict):
        """
        Cria uma nova tabela no banco de dados.

        Args:
            table_name (str): Insira o nome da nova tabela.
            columns (dict): Insira as colunas e seus respectivos formatos no banco de dados.
        """
        con = self.connect()
        cur = con.cursor()
        col_list = ', '.join([f'{col} {datatype}'
                              for col, datatype in columns.items()])
        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({col_list})')
        con.commit()

    def insert_data(self,
                    table_name: str,
                    columns: List[str],
                    data: List[Tuple]):
        """
        Insere dados em uma tabela existente.

        Args:
            table_name (str): Nome da tabela onde os dados serão inseridos.
            columns (list): Lista de colunas onde os dados serão inseridos.
            data (list of tuples): Lista de tuplas contendo os valores a serem inseridos.
        """
        con = self.connect()
        cur = con.cursor()
        col_list = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in columns])
        for row in data:
            cur.execute(
                f'INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})',  # noqa
                row)
        con.commit()
        con.close()


# Exemplo de Uso:
if __name__ == "__main__":
    # Criando uma instância do controlador de banco de dados
    db_controller = ControlDatabases("example.db")

    # Criando uma tabela
    db_controller.create_table("example_table", {"id": "INTEGER PRIMARY KEY",
                                                 "name": "TEXT",
                                                 "age": "INTEGER"})

    # Inserindo dados na tabela
    data_to_insert = [(1, "Alice", 30), (2, "Bob", 25), (3, "Charlie", 35)]
    db_controller.insert_data("example_table", ["id", "name", "age"],
                              data_to_insert)

    # Executando uma consulta SQL e obtendo os resultados como um DataFrame pandas  # noqa
    query_result = db_controller.command("SELECT * FROM example_table",
                                         return_df=True)
    print(query_result)
