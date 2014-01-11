from database.story import Story



class Database:
    def story_list(self):
        stories = self._cursor.execute('''SELECT storyID FROM stories''')
        self._story_list = []
        for s in stories:
            self._story_list.append(story.Story.from_id(s[0]))
        return self._story_list

# Testing code
##db = Database()
##s = db.story_list()[0]
##print(s.title())
##print(s.story_id())
##blah = s.first_word()

# OTHER TEST
s2 = Story.from_id(1)
print('title:', s2.title())
print('id:', s2.story_id())
print('first word:', s2.first_word().value())
