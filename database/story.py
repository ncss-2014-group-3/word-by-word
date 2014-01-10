import sqlite3

class Story:
    def __init__(self, title, first_word, story_id=None):
        self._title = title
        self._first_word = first_word
        self._story_id = story_id
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
    def total_votes(self):
        cursor.execute("""
            SELECT COUNT(*) FROM votes as v 
            INNER JOIN words as m ON v.wordID = m.wordID
            WHERE m.storyID = ?
        """, (self._story_id,))
        
    def story_id(self):
        return self._story_id
    def title(self):
        return self._title
    def save(self):
        if not self._story_id:
            cursor.execute('''INSERT INTO stories (name) VALUES (?)''', (self._title,))
            self._story_id = cursor.lastrowid
