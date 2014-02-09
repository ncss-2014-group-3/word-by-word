from database import connection
from database import word
from sqlite3 import IntegrityError

cursor = connection.cursor()
words = cursor.execute('''
    SELECT
        uw.storyID, uw.parentID, uw.wordID, uw.word
    FROM
        words AS uw
    INNER JOIN
    (
    SELECT
    	storyID, parentID, word, COUNT(*) AS c
    FROM
    	words
    GROUP BY
    	storyID, parentID, word
    HAVING c > 1
    ) AS lw
    ON lw.storyID=uw.storyID
    AND lw.parentID=uw.storyID
    AND lw.word=uw.word
    ORDER BY uw.storyID ASC, uw.wordID ASC
''').fetchall()

story_id = None
for w in words:
    if w[0] != story_id:
        story_id = w[0]
        original_word_id = w[2]
    else:
        try: # Move all votes to original word
            cursor.execute('''
                UPDATE votes
                SET wordID = ?
                WHERE
                    storyID = ?
                    AND wordID = ?
            ''', (original_word_id, story_id, w[2]))
            connection.commit()
        except IntegrityError as e: # Catch if user has already voted for said word
            if e.args == ('columns storyID, wordID, username are not unique',):
                cursor.execute('''
                    DELETE FROM
                        votes
                    WHERE
                        storyID = ?
                        AND wordID = ?
                ''', (story_id, w[2]))
                connection.commit()
            else:
            	raise
        for child in word.Word.from_id(w[2]).children:
            cursor.execute('''
                UPDATE words
                SET parentID = ?
                WHERE
                    storyID = ?
                    AND wordID = ?
            ''', (original_word_id, story_id, child.id)) # Move children to original word
            connection.commit()
        cursor.execute('''
            DELETE FROM
                words
            WHERE
                storyID = ?
                AND wordID = ?
        ''', (story_id, w[2]))
        connection.commit()
