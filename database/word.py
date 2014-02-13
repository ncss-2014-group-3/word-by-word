from . import connection
from . import cached_property
from . import DuplicateWordException


class Word(object):

    @classmethod
    def from_story_id(cla, story_id):
        """
        Get the first word for a story
        """
        c = connection.cursor()
        c.execute('SELECT wordID, storyID, word, author, parentID FROM words WHERE storyID = ? and parentID IS NULL', (story_id,))
        result = c.fetchone()
        if result:
            return cla(*result)

    @classmethod
    def from_id(cla, word_id):
        c = connection.cursor()
        c.execute('''SELECT wordID, storyID, word, author, parentID
                    FROM words
                    WHERE wordID = ?''', (word_id,))
        result = c.fetchone()
        if result:
            return cla(*result)

    def __init__(self, id, story_id, value, author, parent_id=None):
        self.id = id
        self.parent_id = parent_id
        self.story_id = story_id

        self.value = value
        self.author = author

        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM votes WHERE wordID = ?', (self.id,))
        result = cursor.fetchone()

        self._dir_votes = 0
        if result is not None:
            self._dir_votes = result[0]

        if not id:
            cursor.execute('''
                SELECT COUNT(*)
                FROM words
                WHERE
                storyID = ?
                AND parentID = ?
                AND word = ?
            ''', (self.story_id, self.parent_id, self.value))
            same = cursor.fetchone()[0]
            if int(same) == 0:
                self.save()
            else:
                raise DuplicateWordException(
                    self.story_id,
                    self.parent_id,
                    self.value
                )

    def __str__(self):
        return self.value

    def add_child(self, value, author):
        new_word = Word(False, self.story_id, value, author, self.id)
        new_word.save()
        return new_word

    def remove(self):
        for child in self.children:
            child.remove()

        c = connection.cursor()
        c.execute("""
        DELETE FROM words WHERE storyID = ? AND wordID = ?
        """, (self.story_id, self.id,))
        connection.commit()

    @property
    def word_count(self):
        count = 1  # account for self
        for child in self.children:
            count += child.word_count
        return count

    @property
    def votes(self):
        return len(self.voters)

    @cached_property
    def voters(self):
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM votes WHERE storyID=? AND wordID=?', (self.story_id, self.id))

        users = set([u[0] for u in cursor.fetchall()])

        for child in self._children_unsorted:
            users.update(child.voters)

        return users

    #For some reason this does not like being cached
    @property
    def direct_voters(self):
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM votes WHERE storyID=? AND wordID=?', (self.story_id, self.id))

        users = set(cursor.fetchall())
        return users

    def has_voted(self, voter):
        return False if voter is None else (voter.username in self.direct_voters)

    def add_vote(self, voter):
        self._dir_votes += 1
        if self.remove_vote(voter):
            self._dir_votes -= 1

        c = connection.cursor()
        c.execute("""
        INSERT INTO votes (storyID, wordID, username) VALUES (?,?,?)
        """, (self.story_id, self.id, voter.username))
        connection.commit()

    def remove_vote(self, voter):
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM votes WHERE storyID=? AND wordID=? AND username=?',
            (self.story_id, self.id, voter.username)
        )
        connection.commit()

    @property
    def children(self):
        children = self._children_unsorted

        return sorted(children, key=lambda w: w.votes, reverse=True)

    @cached_property
    def _children_unsorted(self):
        c = connection.cursor()
        c.execute("""
            SELECT words.wordID, storyID, word, author, parentID
            FROM words
            WHERE parentID = ?
        """, (self.id,))

        return [Word(*w) for w in c]

    def _deepest_child(self):
        # Depth first, brah.
        m = 0
        for child in self.children:
            m = max(m, child._deepest_child())
        return m + 1

    def fixed(self, n=5):
        return self._deepest_child() > n

    def as_json(self):
        return {
            'value': self.value,
            'id': self.id,
            'parent_id': self.parent_id,
            'author': self.author,
            'children': [
                child.as_json() for child in self.children
            ]
        }

    @property
    def favourite_child(self):
        cursor = connection.cursor()
        cursor.execute('''
            SELECT words.wordID, storyID, word, author, parentID
            FROM words
            WHERE storyID = ? AND parentID = ?
            ORDER BY (SELECT COUNT(*) FROM votes WHERE storyID=? AND wordID=?)
            LIMIT 1''', (self.story_id, self.id, self.story_id, self.id))
        row = cursor.fetchone()
        return None if row is None else Word(*row)

    def fixed_children(self):
        if not self.children:
            return True
        return any(w.fixed() for w in self.children)

    def save(self):
        c = connection.cursor()

        if self.id:
            #print('[save] update')
            c.execute("""
                UPDATE words
                SET
                storyID = ?
                ,word = ?
                ,parentID = ?
                ,author = ?
                WHERE
                    wordID = ?
                """, (self.story_id, self.value, self.parent_id, self.author.username, self.id))
            connection.commit()

        else:
            #print('[save] insert')
            c.execute("""
                INSERT INTO words VALUES (NULL,?,?,?,?)
                """, (self.parent_id, self.story_id, self.value, self.author.username))
            connection.commit()
            self.id = c.lastrowid
