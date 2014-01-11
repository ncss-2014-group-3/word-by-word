import sqlite3,word

class Story:
    @classmethod
    def from_id(cla,id):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT name FROM stories WHERE storyID=?''', (id,))
            row = cursor.fetchone()
            if row is None:
                return False
            cursor.execute('''  SELECT * FROM words
                                WHERE wordID NOT IN (SELECT childID FROM wordchild)
                                AND storyID=?''', (id,))
            word_row = cursor.fetchone()
            return cla(row[0],word.Word(word_row[0],id,word_row[2]),id)
    def __init__(self, title, first_word, story_id=None):
        self._title = title
        self._first_word = first_word
        self._story_id = story_id
        self._connection = sqlite3.connect('database.db')
        self._cursor = self._connection.cursor()
        self._first_word = first_word
    
    def total_votes(self):
        self._cursor.execute('''
            SELECT COUNT(*) FROM votes as v 
            INNER JOIN words as m ON v.wordID = m.wordID
            WHERE m.storyID = ?
        ''', (self._story_id,))
    def story_id(self):
        return self._story_id
    def title(self):
        return self._title
    def save(self):
        if not self._story_id:
            self._cursor.execute('''INSERT INTO stories (name) VALUES (?)''', (self._title,))
            self._story_id = cursor.lastrowid
    def first_word(self):
        return self._first_word
print(Story.from_id(1))
