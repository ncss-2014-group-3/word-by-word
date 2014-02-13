import itertools

from .word import Word
from . import connection


class Story(object):
    @classmethod
    def from_id(cla, id):
        cursor = connection.cursor()
        cursor.execute('''SELECT name FROM stories WHERE storyID = ?''', (id,))
        row = cursor.fetchone()

        if row is None:
            return None

        first_word = Word.from_story_id(id)
        if first_word is None:
            return None

        return cla(row[0], first_word, first_word.author, id)

    @classmethod
    def story_list(cls, limit=10, page=1):
        cursor = connection.cursor()
        stories = cursor.execute('''
            SELECT
                stories.storyID,
                (
                    SELECT COUNT(*)
                    FROM votes
                    INNER JOIN words ON words.storyID = stories.storyID
                    WHERE votes.storyID = words.storyID AND votes.wordID = words.wordID
                ) AS n_votes
            FROM stories
            GROUP BY stories.storyID
            ORDER BY n_votes DESC
            LIMIT ?
            OFFSET ?
        ''', (limit, (page-1)*limit))

        return [
            Story.from_id(s[0])
            for s in stories
        ]

    def __init__(self, title, first_word, author, story_id=None):
        """
        Creates a story
        arguments:
            Title (of story)
            First word (string or word object)
            story id (optional, new story will be created if not specified)
        """
        self.title = title
        self.story_id = story_id
        self._cursor = connection.cursor()
        self.first_word = first_word

        if not self.story_id:
            self._cursor.execute('''INSERT INTO stories (name) VALUES (?)''', (self.title,))
            self.story_id = self._cursor.lastrowid
            connection.commit()

        if type(first_word) == str:
            # author add
            self.first_word = Word(False, self.story_id, first_word, author)
        else:
            self.first_word = first_word

    @property
    def total_votes(self):
        result = self._cursor.execute('''
            SELECT COUNT(*) FROM votes as v 
            INNER JOIN words as m ON v.storyID = m.storyID AND v.wordID = m.wordID
            WHERE m.storyID = ?
        ''', (self.story_id,))
        return result.fetchone()[0]

    def remove(self):
        self.first_word.remove()
        self._cursor.execute('''
            DELETE FROM stories WHERE storyID = ?
        ''', (self.story_id,))
        connection.commit()

    @property
    def word_count(self):
        return self.first_word.word_count

    @property
    def author(self):
        return self.first_word.author

    def walk_first_words(self, num=10):
        return itertools.islice(self.walk_words(), num)

    def walk_words(self):
        word = self.first_word

        while word:
            yield word
            word = word.favourite_child

    def first_non_fixed(self):
        word = self.first_word

        while word.fixed():
            next_word = word.favourite_child
            if next_word is None:
                break
            word = next_word

        return word

    def first_words(self, num=10):
        nwords = []
        for w in self.walk_first_words(num):
            nwords.append(w.value)
        return ' '.join(nwords)

    def save(self):
        self._cursor.execute('''UPDATE stories SET
            name = ?
            WHERE storyID = ?
        ''', (self.title, self.story_id))
        connection.commit()

    def prune(self, n=5):
        len_deepest = self.first_word._deepest_child()
        last_fixed = max(len_deepest - n,0)

        for w in self.walk_first_words(last_fixed):
            for child in w.children[1:]:
                child.remove()
