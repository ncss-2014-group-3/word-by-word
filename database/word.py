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
            
        c.commit()
        return result
        
    def __init__(self, id, story_id, value):
        self._id = id
        self._story_id = story_id
        self._value = value
        
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
        
    def children(self):
        c = db.cursor()
        c.row_factory = dict_factory
        c.execute("""
            SELECT * FROM
                words
            INNER JOIN wordchild ON words.wordID = wordchild.childID
            WHERE
                wordchild.parentID = ?
        """, (self.id(),))
        
        children = {}
        for childWord in c:
            children[childWord["word"]] = Word(childWord["wordID"], childWord["storyID"], childWord["value"])
            
        #c.commit()
        return children
    
    def save(self):
        c = db.cursor()
        if self._id:
            c.execute("""
                UPDATE words
                SET
                storyID = ?
                , word = ?
                """, (self._story_id, self._value))
            db.commit()
        else:
            c.execute("""
                INSERT INTO words VALUES (NULL,?,?)
                """, (self._story_id, self._value))
            db.commit()
        
        
        
testWord = Word.from_id(1)

#testWord.value("world")

print(testWord.value())
        
testWord.save()
   
