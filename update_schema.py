from database import connection
from database import user
from database import word
from sqlite3 import OperationalError

cursor = connection.cursor()

# Hash passwords
try:
    cursor.execute('''ALTER TABLE users ADD COLUMN salt TEXT NULL''')
    connection.commit()
except OperationalError as e:
    if e.args != ('duplicate column name: salt',):
        raise
else:
    results = cursor.execute('''SELECT username,password,salt FROM users''').fetchall()
    for u in results:
        if u[2] is None:
            uo = user.User.from_username(u[0])
            print(uo.username + '\'s password is not hashed (detected NULL salt). Performing hash on password...')
            uo.update(u[1])
            print('Successfully hashed ' + uo.username + '\'s password.')

try:
    cursor.execute('''ALTER TABLE votes ADD COLUMN storyID INTEGER NULL''')
    connection.commit()
except OperationalError as e:
    if e.args != ('duplicate column name: storyID',):
        raise
else:
    cursor.execute('''ALTER TABLE votes RENAME TO votes_old''')
    cursor.execute('''
        CREATE TABLE votes (
            storyID INTEGER NOT NULL
            ,wordID  INTEGER NOT NULL
            ,username TEXT NOT NULL
            ,PRIMARY KEY (storyID, wordID, username)
            ,FOREIGN KEY(storyID) REFERENCES stories(storyID)
            ,FOREIGN KEY(wordID) REFERENCES words(wordID)
        )
    ''')
    old_votes = cursor.execute('''
        SELECT
            wordID, username
        FROM votes_old
    ''').fetchall()
    for v in old_votes:
    	word_inst = word.Word.from_id(v[0])
    	if word_inst is not None:
        	cursor.execute('''
            	INSERT INTO
                	votes
            	(storyID, wordID, username)
            	VALUES(?,?,?)
        	''', (word_inst.story_id, v[0], v[1]))
    cursor.execute('DROP TABLE votes_old')
