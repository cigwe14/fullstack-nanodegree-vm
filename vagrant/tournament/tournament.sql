-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS Tournament;
CREATE DATABASE Tournament;
\c tournament;

CREATE TABLE Players(Id Serial PRIMARY KEY, 
                     Name VARCHAR(100));

CREATE TABLE Matches(Id Serial PRIMARY KEY, 
                        WinPlayerId INTEGER REFERENCES Players(Id) NOT NULL, 
                        LosePlayerId INTEGER REFERENCES Players(Id) NOT NULL,
                        UNIQUE (WinPlayerId, LosePlayerId));


