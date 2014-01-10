CREATE TABLE stories (
     storyID INTEGER PRIMARY KEY
    ,name    TEXT    NOT NULL
);

CREATE TABLE words (
    wordID  INTEGER PRIMARY KEY
    ,storyID    INTEGER NOT NULL
    ,word   TEXT    NOT NULL
    ,FOREIGN KEY(storyID) REFERENCES stories(storyID)
);

CREATE TABLE wordchild (
    parentID    INTEGER NULL
    ,childID    INTEGER NULL
    ,PRIMARY KEY(parentID, childID)
    ,FOREIGN KEY(parentID) REFERENCES words(wordID)
    ,FOREIGN KEY(childID) REFERENCES words(wordID)
);

CREATE TABLE votes (
    wordID  INTEGER NOT NULL
    ,FOREIGN KEY(wordID) REFERENCES words(wordID)
);