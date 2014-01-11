import database
db = database.Database()
for story_obj in db.story_list():
    print('Title:',story_obj.title())
    print('Votes:',story_obj.total_votes())
    print('First word:',story_obj.first_word().value())
    print('Word count:',story_obj.word_count()) # Not Implemented
