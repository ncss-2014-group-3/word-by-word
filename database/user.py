import sqlite3, hashlib, random, string
from . import connection
from database import userStats
from database.story import Story


def cached_property(f):
    """returns a cached property that is calculated by function f"""
    def get(self): #webscale
        try:
            return self._property_cache[f]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[f] = f(self)
            return x
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x
        
    return property(get)

class User:
    @classmethod
    def from_username(cla, username):
        cursor = connection.cursor()
        returned = cursor.execute('SELECT username,fullname FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        if row: # user exists
            return cla(username) # return User object
        else: # user does not exist
            return None

    @classmethod
    def login(cla, username, password):
        check = ''
        cursor = connection.cursor()
        returned = cursor.execute('SELECT password,salt FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        if row is None:
            return False
        h = hashlib.sha256()
        if password == hashlib.sha256((row[0]+str(row[1])).encode('utf-8')).hexdigest(): # check inputted against returned password from db
            return cla(username) # return User object if True
        else:
            return False

    @classmethod
    def create(cla, username, password, fullname='User', email=''):
        cursor = connection.cursor()
        returned = cursor.execute('''SELECT username FROM users WHERE username=?''', (username,))
        row = returned.fetchone()
        if row:
            return False # user exists
        elif row is None: # User does not exist, insert a new user into database
            salt = ''
            for i in range(32):
                salt += random.choice(string.printable)
            password = hashlib.sha256((password+salt).encode('utf-8')).hexdigest()
            cursor.execute('''INSERT INTO users VALUES(?,?,?,?,?)''', (username, password, fullname, email, salt))
            connection.commit()
            return cla(username) # return User object
    @classmethod
    def user_list(cls, limit=10):
        cursor = connection.cursor()
        users = cursor.execute('''
            SELECT username, SUM(c) AS s FROM
            (
                SELECT users.username, COUNT(DISTINCT words.wordID) AS C FROM USERS
                LEFT OUTER JOIN words ON words.author = users.username
                LEFT OUTER JOIN votes ON votes.wordID = words.wordID
                GROUP BY words.wordID
            )
            GROUP BY username
            ORDER BY s DESC
            LIMIT ?''', (limit,))
        user_list = []
        for u in users:
            user_list.append(User.from_username(u[0]))
        return user_list
    
    def __init__(self, username):
        self.username = username
        self.stats = userStats.Stats(username)

    def remove(self):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE username=?''', (self.username,))
        connection.commit()

    def update(self, new_password, fullname='User'):
        salt = ''
        for i in range(32):
            salt += random.choice(string.printable)
        new_password = hashlib.sha256((new_password+salt).encode('utf-8')).hexdigest()
        cursor = connection.cursor()
        cursor.execute('''UPDATE users SET password=?, fullname=?, salt=? WHERE username=?''', (new_password, fullname, salt, self.username))
        connection.commit()

    @property
    def score(self):
        cursor = connection.cursor()
        returnedvotes = cursor.execute('''SELECT COUNT(wordID) FROM votes WHERE wordID IN
                                        (SELECT wordID FROM words WHERE author=?)''', (self.username,))
        score = returnedvotes.fetchone()[0]
        return score

    @property
    def email(self):
        cursor = connection.cursor()
        returned = cursor.execute('''SELECT email FROM users WHERE username=? ''', (self.username,))
        email = returned.fetchone()[0]
        return email
        
    @property
    def image_url(self):
        size = 200
        return 'http://www.gravatar.com/avatar/' + hashlib.md5(self.email.encode()).hexdigest() + '.png?s='+str(size)

    @property
    def own_stories(self):
        cursor = connection.cursor()
        returnedstories = cursor.execute('''
                                        SELECT storyID from stories WHERE storyID IN
                                        (
                                            SELECT storyID FROM words WHERE author=? AND parentID IS NULL
                                        )
                                        ''', (self.username,))
        stories = [Story.from_id(x[0]) for x in returnedstories.fetchall()]
        return stories

    @cached_property
    def top_story(self):
        cursor = connection.cursor()
        result = cursor.execute("""
            SELECT
                storyID,
                (
                SELECT count(*) FROM votes
                WHERE votes.wordID IN
                    (SELECT wordID FROM words WHERE words.storyID = stories.storyID)
                ) as totalVotes
                ,(
                SELECT author FROM words WHERE words.storyID = stories.storyID AND
                    parentID IS NULL
                ) as sauthor
            FROM stories
            WHERE sauthor = ?
            ORDER BY totalVotes DESC
            LIMIT 1
        """, (self.username,))
        story = result.fetchone()
        if story is not None:
            return Story.from_id(story[0])
        return None
        
