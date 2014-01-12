DROP TABLE IF EXISTS stories;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS wordchild;
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS users;

CREATE TABLE stories (
     storyID INTEGER PRIMARY KEY
    ,name    TEXT    NOT NULL
);

CREATE TABLE words (
    wordID  INTEGER PRIMARY KEY
    ,parentID   INTEGER NULL
    ,storyID    INTEGER NOT NULL
    ,word   TEXT    NOT NULL
);


CREATE TABLE votes (
    wordID  INTEGER NOT NULL
    ,FOREIGN KEY(wordID) REFERENCES words(wordID)
);

CREATE TABLE users (
    username TEXT NOT NULL PRIMARY KEY
    ,password TEXT NOT NULL
);