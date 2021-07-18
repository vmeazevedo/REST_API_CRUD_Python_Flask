import sqlite3

conn = sqlite3.connect("livros.sqlite")

# PARAMETROS DE CONFIG DO BD
cursor = conn.cursor()
sql_query = """ CREATE TABLE livros (
    id integer PRIMARY KEY,
    autor text NOT NULL,
    lingua text NOT NULL,
    titulo text NOT NULL
)"""
cursor.execute(sql_query)
