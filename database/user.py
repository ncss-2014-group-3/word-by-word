import hashlib
import random
import string

from . import connection
from . import cached_property
from database.story import Story
from database.word import Word


def password_hash(password, salt):
    return hashlib.sha256((password+salt).encode('utf-8')).hexdigest()


class User(object):
    @classmethod
    def from_username(cla, username):
        cursor = connection.cursor()
        returned = cursor.execute('SELECT username,fullname FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        if row:  # user exists
            return cla(username)  # return User object
        else:  # user does not exist
            return None

    @classmethod
    def login(cla, username, password):
        cursor = connection.cursor()
        returned = cursor.execute('SELECT password,salt FROM users WHERE username=?', (username,))
        row = returned.fetchone()
        if row is None:
            return False

        hashed = hashlib.sha256((password+row[1]).encode('utf-8')).hexdigest()

        # check inputted against returned password from db
        if row[0] == hashed:
            return cla(username)  # return User object if True
        else:
            return False

    @classmethod
    def create(cla, username, password, fullname='User', email=''):
        cursor = connection.cursor()
        returned = cursor.execute('''SELECT username FROM users WHERE username=?''', (username,))
        row = returned.fetchone()
        if row:
            return False  # user exists

        elif row is None:
            # User does not exist, insert a new user into database
            salt = ''
            for i in range(32):
                salt += random.choice(string.printable)
            password = password_hash(password, salt)

            cursor.execute(
                '''INSERT INTO users VALUES(?,?,?,?,?)''',
                (username, password, fullname, email, salt)
            )
            connection.commit()
            return cla(username)  # return User object

    @classmethod
    def user_list(cls, limit=10):
        cursor = connection.cursor()
        users = cursor.execute('''
            SELECT
                users.username,count(votes.username) AS totalVotes
            FROM
                users
            LEFT OUTER JOIN
                words ON users.username=author
            LEFT OUTER JOIN
                votes ON words.wordID=votes.wordID
            GROUP BY
                users.username
            ORDER BY
                totalVotes DESC
            LIMIT ?
        ''', (limit,))
        user_list = []
        for u in users:
            user_list.append(User.from_username(u[0]))
        return user_list

    def __init__(self, username):
        self.username = username

    def remove(self):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE username=?''', (self.username,))
        connection.commit()

    def update(self, new_password, fullname='User'):
        salt = ''
        for i in range(32):
            salt += random.choice(string.printable)
        new_password = password_hash(new_password, salt)
        cursor = connection.cursor()
        cursor.execute('''UPDATE users SET password=?, fullname=?, salt=? WHERE username=?''', (new_password, fullname, salt, self.username))
        connection.commit()

    @property
    def score(self):
        cursor = connection.cursor()
        result = cursor.execute('''
            SELECT COUNT(votes.wordID)
            FROM users
            INNER JOIN words ON users.username=words.author
            INNER JOIN votes ON words.wordID=votes.wordID
            WHERE words.author = ?
        ''', (self.username,))
        return result.fetchone()[0]

    @property
    def email(self):
        cursor = connection.cursor()
        returned = cursor.execute('''SELECT email FROM users WHERE username=? ''', (self.username,))
        email = returned.fetchone()[0]
        return email

    @property
    def image_url(self):
        size = 200

        return 'http://www.gravatar.com/avatar/{}.png?s={}'.format(
            hashlib.md5(self.email.encode()).hexdigest(),
            size
        )

    @property
    def own_stories(self):
        cursor = connection.cursor()
        returnedstories = cursor.execute('''
                                        SELECT storyID from stories WHERE storyID IN
                                        (
                                            SELECT storyID FROM words WHERE author=? AND parentID IS NULL
                                        )
                                        ''', (self.username,))

        return [
            Story.from_id(story[0])
            for story in returnedstories.fetchall()
        ]

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

    @property
    def total_words(self):
        cursor = connection.cursor()
        result = cursor.execute('''
            SELECT
                COUNT(*)
            FROM words
            WHERE
                author = ?
        ''', (self.username,))
        return result.fetchone()[0]

    @property
    def total_stories(self):
        cursor = connection.cursor()
        result = cursor.execute('''
            SELECT
                 COUNT(*)
            FROM stories
            INNER JOIN words ON stories.storyID = words.storyID
            WHERE
                words.parentID IS NULL
                AND words.author = ?
        ''', (self.username,))
        return result.fetchone()[0]

    @property
    def total_stories_contributed(self):
        cursor = connection.cursor()
        result = cursor.execute('''
            SELECT
                 COUNT(DISTINCT storyID)
            FROM (
                SELECT storyID FROM words
                WHERE words.author = ?
            )
        ''', (self.username,))
        return result.fetchone()[0]

    @cached_property
    def best_words(self):
        cursor = connection.cursor()
        result = cursor.execute('''
            SELECT words.wordID, wordVotes
            FROM words
            INNER JOIN (
                SELECT
                    words.wordID as wID, COUNT(votes.wordID) as wordVotes
                FROM
                    votes
                LEFT JOIN words on words.wordID=votes.wordID
                WHERE words.author = ?
                GROUP BY words.wordID
            ) ON words.wordID=wID
            GROUP BY wordID
            HAVING wordVotes=(
                SELECT
                    COUNT(votes.wordID) as wordVotes
                FROM
                    votes
                LEFT JOIN words on words.wordID=votes.wordID
                WHERE words.author = ?
                GROUP BY votes.wordID
                ORDER BY COUNT(votes.wordID) DESC
                LIMIT 1
            )
            LIMIT ?
        ''', (self.username, self.username, 5))
        results = result.fetchall()
        if not results:
            return None

        words = []
        for w in results:
            words.append(Word.from_id(w[0]))

        return words, w[1]

    @property
    def votes_cast(self):
        cursor = connection.cursor()
        result = cursor.execute('''
            SELECT count(*) FROM votes
            WHERE username = ?
        ''', (self.username,))
        return result.fetchone()[0]

    @cached_property
    def frequent_words(self):
        cursor = connection.cursor()
        query = cursor.execute('''
            SELECT LOWER(word)
            FROM words
            WHERE author = ?
            GROUP BY LOWER(word)
            HAVING COUNT(*) = (
                SELECT COUNT(LOWER(word)) as wordCount
                FROM words
                WHERE author = ?
                GROUP BY LOWER(word)
                ORDER BY wordCount DESC
                LIMIT 1
            )
            ORDER BY LOWER(word) ASC
            LIMIT ?
        ''', (self.username, self.username, 5))
        results = query.fetchall()

        words = []
        for w in results:
            words.append(w[0])

        return words
