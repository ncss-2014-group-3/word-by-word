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
            return None
        first_word = Word.from_story_id(id)
        if first_word is None:
            return None
        return cla(row[0], first_word, id)

    @classmethod
    def story_list(cls):
        cursor = connection.cursor()
        stories = cursor.execute('''SELECT storyID FROM stories''')
        stories_list = []
        for s in stories:
            stories_list.append(Story.from_id(s[0]))
        return stories_list
            
    def __init__(self, title, first_word, story_id=None):
        """
        Creates a story
        arguments: 
            Title (of story)
            First word (string or word object)
            story id (optional, new story will be created if not specified)
        """
        self.title = title
        self.story_id = story_id
        self._cursor = connection.cursor()
        self.first_word = first_word
        if not self.story_id:
            self._cursor.execute('''INSERT INTO stories (name) VALUES (?)''', (self.title,))
            self.story_id = self._cursor.lastrowid
            connection.commit()
        if type(first_word) == str:
            self.first_word = Word(False, self.story_id, first_word) #author add
        else:
            self.first_word = first_word
    
    @property
    def total_votes(self):
        self._cursor.execute('''
            SELECT COUNT(*) FROM votes as v 
            INNER JOIN words as m ON v.wordID = m.wordID
            WHERE m.storyID = ?
        ''', (self.story_id,))

    def remove(self):
        self.first_word.remove()
        self._cursor.execute('''
            DELETE FROM stories WHERE storyID = ?
        ''', (self.story_id,))
        connection.commit()
        
    @property
    def word_count(self):
        return self.first_word.word_count
        
    def save(self):
        self._cursor.execte("""UPDATE stories SET
            name = ?
            WHERE storyID = ?
        """, self.title, self.story_id)
        connection.commit()
