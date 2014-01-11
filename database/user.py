import sqlite3, hashlib
from . import connection

class User:
    @classmethod
    def from_username(cla, username):
        cursor = connection.cursor()
        cursor.execute('''SELECT password FROM users WHERE username=?''', (username,))
        row = cursor.fetchone()
        if row is None: 
            return None
        return cla(username, row[0])

    @classmethod
    def login(cla, username, password):
        check = ''
        cursor = connection.cursor()
        returned = cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        for item in returned:
            check = item[0]
        if password == check:
            return cla(username, password)
        else:
            return False
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        cursor = connection.cursor()
        selection = cursor.execute('''SELECT username FROM users''')
        user_list = [x[0] for x in selection]
        if username not in user_list:
            cursor.execute('''INSERT INTO users VALUES(?,?)''', (username, password))
            connection.commit()

    def remove(self):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE username=?''', (self.username,))
        connection.commit()
