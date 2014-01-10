from collections import deque
import sqlite3
db = sqlite3.connect('database.db')

class Story:
    def __init__(self, story_id, title, first_word):
        self._story_id = story_id
        self._title = title
        self._first_word = first_word
    def total_votes(self):
        cursor = db.cursor()
        cursor.execute('''SELECT COUNT(*) FROM votes WHERE storyID=?''', (self._story_id))
    def story_id(self):
        return self._story_id
    def title(self):
        return self._title
    
    def story(self):
        return ' '.join(self._story)
