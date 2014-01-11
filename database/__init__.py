import sqlite3

connection = sqlite3.connect('database.db')

def create():
  create_sql = open('database/createDatabase.sql').read()
  cursor = connection.cursor()
  for statement in create_sql.split(';'):
    cursor.execute(statement)

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
