import sqlite3, hashlib
from . import connection

class User:
    @classmethod
    def from_username(cla, username):
        cursor = connection.cursor()
        returned = cursor.execute('SELECT username FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        if row: # user exists
            returned2 = cursor.execute('SELECT fullname FROM users where username=?', (username,))
            fullnamerow = returned2.fetchone()
            return cla(username, fullnamerow[0]) # return User object
        else: # user does not exist
            return None

    @classmethod
    def login(cla, username, password):
        check = ''
        cursor = connection.cursor()
        returned = cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        check = row[0]
        
        if password == check:
            return cla(username) # return User object if True
        else:
            return False

    @classmethod
    def create(cla, username, password, fullname='User'):
        cursor = connection.cursor()
        returned = cursor.execute('''SELECT username FROM users WHERE username=?''', (username,))
        row = returned.fetchone()
        if row:
            return False # user exists
        elif row is None: # User does not exist, insert a new user into database
            cursor.execute('''INSERT INTO users VALUES(?,?,?)''', (username, password, fullname))
            connection.commit()
            return cla(username, fullname) # return User object
    
    def __init__(self, username, fullname = 'User'):
        self.username = username
        self.fullname = fullname

    def remove(self):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE username=?''', (self.username,))
        connection.commit()

    def update(self, username, old_password, new_password):
        cursor = connection.cursor()
        cursor.execute('''UPDATE users SET password=? WHERE username=? AND password=?''', (new_password, username, old_password))
        connection.commit()
