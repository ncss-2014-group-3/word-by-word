import sqlite3

class Database:
    def __init__(self):
        self._connection = sqlite3.connect('database.db')
        self._cursor = self._connection.cursor()
    
    def story_list(self):
        self._cursor.execute('''SELECT name FROM stories''')
        stories = [story[0] for story in self._cursor] #story[0] gets the 1st value of the tuple (title)
        return stories
