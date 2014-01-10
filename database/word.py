import sqlite3

db = sqlite3.connect("database.db")


class Word:
    @classmethod
    def word_by_id(cla, word_id):
        c = db.cursor()
        c.execute("SELECT wordID, storyID, word FROM words WHERE wordID = ?", (word_id,))
        result = c.fetchone()
        if result:
            return cla(result["wordID"],result["storyID"], result["word"])
            
        c.commit()
        return result
        
    def __init__(self, id, story_id, word):
        self._id = id
        self._story_id = story_id
        self._word = word
        
   