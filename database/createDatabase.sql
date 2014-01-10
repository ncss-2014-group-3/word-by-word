CREATE TABLE stories (
     storyID INTEGER NOT NULL
    ,name    TEXT    NOT NULL
    ,PRIMARY KEY (storyID)
);

CREATE TABLE words (
    wordID  INTEGER NOT NULL
    ,storyID    INTEGER NOT NULL
    ,word   TEXT    NOT NULL
    ,PRIMARY KEY (wordID)
    ,FOREIGN KEY(storyID) REFERENCES stories(storyID)
);

CREATE TABLE wordchild (
    parentID    INTEGER NOT NULL
    ,childID    INTEGER NOT NULL
    ,PRIMARY KEY(parentID, childID)
    ,FOREIGN KEY(parentID) REFERENCES words(wordID)
    ,FOREIGN KEY(childID) REFERENCES words(wordID)
);

CREATE TABLE votes (
    wordID  INTEGER NOT NULL
    ,FOREIGN KEY(wordID) REFERENCES words(wordID)
);