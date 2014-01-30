from . import connection
from . import cached_property


class Word:
    @classmethod
    def from_story_id(cla, story_id):
        """
        Get the first word for a story
        """
        c = connection.cursor()
        c.execute("SELECT wordID, storyID, word, author, parentID FROM words WHERE storyID = ? and parentID IS NULL", (story_id,))
        result = c.fetchone()
        if result:
            return cla(*result)

    @classmethod
    def from_id(cla, word_id):
        c = connection.cursor()
        c.execute("""SELECT wordID, storyID, word, author, parentID
                    FROM words
                    WHERE wordID = ?""", (word_id,))
        result = c.fetchone()
        if result:
            return cla(*result)

    def __init__(self, id, story_id, value, author, parent_id=None):
        self.id = id
        self.parent_id = parent_id
        self.story_id = story_id
        self.value = value
        self.author = author

        c = connection.cursor()
        c.execute("""SELECT count(*) FROM votes WHERE wordID = ?""", (self.id,))
        result = c.fetchone()
        self._dir_votes = 0
        if result is not None:
            #print(self.value, result[0], self.id)
            self._dir_votes = result[0]
        if not id:
            self.save()

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
        DELETE FROM words WHERE wordID = ?
        """, (self.id,))
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
        users = set()
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM votes WHERE wordID=?', (self.id,))
        for user in cursor.fetchall():
            users.add(user)
        for child in self._children_unsorted:
            users.update(child.voters)
        return users

    def add_vote(self, voter):
        self._dir_votes += 1
        if self.remove_vote(voter):
            self._dir_votes -= 1
        c = connection.cursor()
        c.execute("""
        INSERT INTO votes VALUES (?,?)
        """, (self.id, voter.username))
        connection.commit()

    def remove_vote(self, voter):
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM votes WHERE wordID=? AND username=?',
            (self.id, voter.username)
        )
        connection.commit()

    @property
    def children(self):
        children = self._children_unsorted
        children = sorted(children, key=lambda w: w.votes, reverse=True)
        return children

    @cached_property
    def _children_unsorted(self):
        c = connection.cursor()
        c.execute("""
            SELECT words.wordID, storyID, word, author, parentID
            FROM words
            WHERE parentID = ?
        """, (self.id,))

        children = []
        for childWord in c:
            #id, parentID, storyID, word
            children.append(Word(childWord[0], childWord[1], childWord[2], childWord[3], childWord[4]))        
        return children
        
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
            WHERE parentID = ?
            ORDER BY (SELECT COUNT(*) FROM votes WHERE wordID=?)
            LIMIT 1''', (self.id,self.id))
        row = cursor.fetchone()
        return None if row is None else Word(row[0], row[1], row[2], row[3], row[4])

    def _deepest_child(self):
        # Depth first, brah.
        m = 0
        for child in self.children:
            m = max(m, child._deepest_child())
        return m + 1

    def fixed(self, n=5):
        return self._deepest_child() > n

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
