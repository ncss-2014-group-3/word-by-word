import sqlite3, story, word

class Database:
    def __init__(self):
        self._connection = sqlite3.connect('database.db')
        self._cursor = self._connection.cursor()
    
    def story_list(self):
        stories = self._cursor.execute('''SELECT storyID FROM stories''')
        self._story_list = []
        for s in stories:
            self._story_list.append(story.Story.from_id(s[0]))
        return self._story_list


# Testing code
db = Database()
s = db.story_list()[0]
print(s.title())
print(s.story_id())
blah = s.first_word()
#             cursor = self._cursor.execute('''SELECT COUNT(*) FROM words where storyID=?''', (s[0],))

# OTHER TEST
s2 = story.Story.from_id(1)
print('title:', s2.title())
print('id:', s2.story_id())
print('first word:', s2.first_word().value())
