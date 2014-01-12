import sqlite3, hashlib
from . import connection

class User:
    @classmethod
    def from_username(cla, username):
        return cla(username)

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
    def create(cla, username, password):
        cursor = connection.cursor()
        returned = cursor.execute('''SELECT username FROM users WHERE username=?''', (username,))
        row = returned.fetchone()
        if row:
            return False # user exists
        elif row is None: # User does not exist, insert a new user into database
            cursor.execute('''INSERT INTO users VALUES(?,?)''', (username, password))
            connection.commit()
            return cla(username) # return User object
        pass
    
    def __init__(self, username):
        self.username = username

    def remove(self):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE username=?''', (self.username,))
        connection.commit()

    def update(self, username, old_password, new_password):
        cursor = connection.cursor()
        cursor.execute('''UPDATE users SET password=? WHERE username=? AND password=?''', (new_password, username, old_password))
        connection.commit()
