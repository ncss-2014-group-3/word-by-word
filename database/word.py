import sqlite3

db = sqlite3.connect("database.db")

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Word:
    @classmethod
    def from_id(cla, word_id):
        c = db.cursor()
        c.execute("SELECT wordID, storyID, word FROM words WHERE wordID = ?", (word_id,))
        result = c.fetchone()
        if result:
            return cla(result[0],result[1], result[2])
            
        return False
        
    def __init__(self, id, story_id, value):
        self._id = id
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
        new_word = Word(False, self.story_id(), value)
        new_word.save()
        c = db.cursor()
        c.execute("""
        INSERT INTO wordchild VALUES (?,?)
        """, (self._id, new_word._id))
        db.commit()
        return new_word
    def remove(self):
        for child in self.children():
            child.remove()
        c = db.cursor()
        c.execute("""
        DELETE FROM words WHERE wordID = ?
        """, (self._id,))
        c.execute("""
        DELETE FROM wordchild WHERE parentID = ?
        """, (self._id,))
        db.commit()
        
    def word_count(self):
        count = 1 #account for self
        for child in self.children():
            count += child.word_count()
        return count
    
    def children(self):
        c = db.cursor()
        
        c.execute("""
            SELECT * FROM
                words
            INNER JOIN wordchild ON words.wordID = wordchild.childID
            WHERE
                wordchild.parentID = """ + str(self._id) + """
        """)
        
        
        
        children = []
        for childWord in c:
            children.append(Word(childWord[0], childWord[1], childWord[2]))
        
        return children
    
    def save(self):
        c = db.cursor()
        if self._id:
            print('[save] update')
            c.execute("""
                UPDATE words
                SET
                storyID = ?
                , word = ?
                WHERE
                    wordID = ?
                """, (self._story_id, self._value, self._id))
            db.commit()
        else:
            print('[save] insert')
            c.execute("""
                INSERT INTO words VALUES (NULL,?,?)
                """, (self._story_id, self._value))
            db.commit()
            self._id = c.lastrowid
        
        
        
   