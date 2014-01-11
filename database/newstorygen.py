import sqlite3

class NewStoryGen:
    def __init__(self,db_name):
        conn = sqlite3.connect(db_name)
        self.cur = conn.cursor()
                
    def add_story(self,title,word):
        # may need to do some checks here
        
        #start a new story 
        self.cur.execute('INSERT INTO stories VALUES({0},{1})'.format(title, word))
        self.cur.commit()
        
        #get the most recent storyid FIXME:assumes we are referring to the last insert
        s = self.cur.execute('SELECT storyID FROM stories ORDER BY storyID DESC LIMIT 1').fetchone()[0] 
        
        return s
