import sqlite3
from .word import Word
from . import connection

class Story:
    @classmethod
    def from_id(cla,id):
        cursor = connection.cursor()
        cursor.execute('''SELECT name FROM stories WHERE storyID=?''', (id,))
        row = cursor.fetchone()
        if row is None:
            return False
        cursor.execute('''  SELECT * FROM words
                            WHERE parentID IS NULL
                            AND storyID=?''', (id,))
        word_row = cursor.fetchone()
        return cla(row[0], Word(word_row[0],id,word_row[2]),id)

    @classmethod
    def story_list(self):
        stories = self._cursor.execute('''SELECT storyID FROM stories''')
        stories_list = []
        for s in stories:
            stories_list.append(Story.from_id(s[0]))
        return stories_list
            
    def __init__(self, title, first_word, story_id=None):
        self._title = title
        self._story_id = story_id
        self._cursor = connection.cursor()
        self._first_word = first_word
        if not self._story_id:
            self._cursor.execute('''INSERT INTO stories (name) VALUES (?)''', (self._title,))
            connection.commit()
            self._story_id = self._cursor.lastrowid
        if type(first_word) == str:
            self._first_word = Word(False, self._story_id, first_word)
        else:
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
            
    def first_word(self):
        return self._first_word
        
    def remove(self):
        self._first_word.remove()
        self._cursor.execute('''
            DELETE FROM stories WHERE storyID = ?
        ''', (self._story_id,))
        connection.commit()
        
    def word_count(self):
        return self._first_word.word_count()

if __name__ == '__main__':
    # Test
    s = Story.from_id(1)
    print('title:', s.title())
    print('id:', s.story_id())
    print('first word:', s.first_word().value())

    # Doesn't work D:
    print('\nNot working D:')
    print(s.first_word().children())
