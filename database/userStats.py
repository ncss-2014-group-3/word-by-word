from . import connection

class Stats:
    def __init__(self, username):
        self.username = username
        
    @property
    def total_words(self):
        c = connection.cursor()
        result = c.execute("""
            SELECT count(*) FROM words WHERE author = ?
        """, (self.username,))
        return result.fetchone()[0]
        
    @property
    def total_stories_created(self):
        c = connection.cursor()
        result = c.execute("""
            SELECT
                 count(*)
            FROM stories
            INNER JOIN words ON stories.storyID = words.storyID
            WHERE
                words.parentID IS NULL
                AND words.author = ?
        """, (self.username,))
        return result.fetchone()[0]
        
    @property
    def total_stories_contributed(self):
        c = connection.cursor()
        result = c.execute("""
            SELECT
                 count(*)
            FROM stories
            WHERE storyID IN (
                SELECT storyID FROM words
                WHERE words.author = ?
            )
        """, (self.username,))
        return result.fetchone()[0]
        
    @property
    def most_upvoted_word(self):
        print('asdf')
        c = connection.cursor()
        result = c.execute("""
            SELECT
                 word
                ,(SELECT count(*) FROM votes WHERE votes.wordID = words.wordID) as wordVotes
            FROM words
            WHERE words.author = ?
            ORDER BY wordVotes DESC
            LIMIT 1
        """, (self.username,))
        results = result.fetchone()
        if results is not None:
            return results[0]
        else:
            return "No upvoted words"
        
    @property
    def total_votes(self):
        c = connection.cursor()
        result = c.execute("""
            SELECT count(*) FROM votes
            WHERE username = ?
        """, (self.username,))
        return result.fetchone()[0]
    
    @property
    def frequent_word(self):
        c = connection.cursor()
        query = c.execute("""
            SELECT word, count(word) as wordCount FROM words
            WHERE author = ?
            GROUP BY word
            ORDER BY wordCount DESC
            LIMIT 1
        """, (self.username,))
        result = query.fetchone()
        if result is not None:
            return result[0]
        else:
            return "No frequent words"
        
    
    @property
    def top_story(self):
        c = connection.cursor()
        query = c.execute("""
            SELECT
                name,
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
        result = query.fetchone()
        if result is not None:
            return result[0]
        return "No top stories"
        
        
        
        
        
        
        
        