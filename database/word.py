import sqlite3

from . import connection, dict_factory

class Word:
    @classmethod
    def from_id(cla, word_id):
        c = connection.cursor()
        c.execute("SELECT wordID, storyID, word, parentID FROM words WHERE wordID = ?", (word_id,))
        result = c.fetchone()
        if result:
            return cla(result[0],result[1], result[2], result[3])
            
        return False
        
    def __init__(self, id, story_id, value, parent_id = None):
        self._id = id
        self._parent_id = parent_id
        self._story_id = story_id
        self._value = value
        if not id:
            self.save()
        
    def id(self):
        return self._id
       
    def story_id(self, new_value=None):
        if new_value is not None:
            self._value = new_value
        return self._story_id
    
    def value(self, new_value=None):
        if new_value is not None:
            self._value = new_value
            
        return self._value
        
    def __str__(self):
        return self.value()
        
    def add_child(self, value):
        new_word = Word(False, self.story_id(), value, self._id)
        new_word.save()
        return new_word
    def remove(self):
        for child in self.children():
            child.remove()
        c = connection.cursor()
        c.execute("""
        DELETE FROM words WHERE wordID = ?
        """, (self._id,))
        connection.commit()
        
    def word_count(self):
        count = 1 #account for self
        for child in self.children():
            count += child.word_count()
        return count
    
    def children(self):
        c = connection.cursor()
        
        c.execute("""
            SELECT * FROM
                words
            WHERE
                parentID = """ + str(self._id) + """
        """)
        
        children = []
        for childWord in c:
            #id, parentID, storyID, word
            children.append(Word(childWord[0], childWord[2], childWord[3], childWord[1]))
        
        return children
    
    def save(self):
        c = connection.cursor()
        if self._id:
            #print('[save] update')
            c.execute("""
                UPDATE words
                SET
                storyID = ?
                ,word = ?
                ,parentID = ?
                WHERE
                    wordID = ?
                """, (self._story_id, self._value, self._parent_id, self._id))
            connection.commit()
        else:
            #print('[save] insert')
            c.execute("""
                INSERT INTO words VALUES (NULL,?,?,?)
                """, (self._parent_id, self._story_id, self._value))
            connection.commit()
            self._id = c.lastrowid