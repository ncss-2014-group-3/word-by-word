import sqlite3
from . import connection
from database import userStats

class User:
    @classmethod
    def from_username(cla, username):
        cursor = connection.cursor()
        returned = cursor.execute('SELECT username,fullname FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        if row: # user exists
            return cla(username) # return User object
        else: # user does not exist
            return None

    @classmethod
    def login(cla, username, password):
        check = ''
        cursor = connection.cursor()
        returned = cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        if row is None:
            return False
        if password == row[0]: # check inputted against returned password from db
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
            return cla(username) # return User object
    @classmethod
    def user_list(cls, limit=10):
        cursor = connection.cursor()
        stories = cursor.execute('''
            SELECT username, SUM(c) AS s FROM
            (
                SELECT users.username, COUNT(DISTINCT words.wordID) AS C FROM USERS
                LEFT OUTER JOIN words ON words.author = users.username
                LEFT OUTER JOIN votes on votes,wordID = words.wordID
                GROUP BY words.wordID
            )
            GROUP BY username
            ORDER BY s DESC
            LIMIT ?''', (limit,))
        stories_list = []
        for s in stories:
            stories_list.append(Story.from_id(s[0]))
        return stories_list
    
    def __init__(self, username):
        self.username = username
        self.stats = userStats.Stats(username)

    def remove(self):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE username=?''', (self.username,))
        connection.commit()

    def update(self, username, new_password, fullname='User'):
        cursor = connection.cursor()
        cursor.execute('''UPDATE users SET password=?, fullname=? WHERE username=?''', (new_password, fullname, username))
        connection.commit()

    def get_score(self, username):
        cursor = connection.cursor()
        returnedvotes = cursor.execute('''SELECT COUNT(wordID) FROM votes WHERE wordID IN
                                        (SELECT wordID FROM words WHERE author=?)''', (username,))
        score = returnedvotes.fetchone()[0]
        return score
