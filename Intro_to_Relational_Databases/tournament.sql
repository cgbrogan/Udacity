-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- CREATE TABLE posts ( content TEXT,
--                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--                     id SERIAL );
--
--
-- once complete, use 'psql i\ tournament.sql' within the CLI to import the whole file at once
--
-- clear database initially to test code
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players(
ID serial primary key,
Name text
);

CREATE TABLE matches(
ID serial references players,
Result text
);
