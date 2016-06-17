-- Table definitions for the tournament project.
--

-- remove any existing database or tables
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

-- creates the tournament database
CREATE DATABASE tournament;

-- connects to the database
\c tournament

-- creates a table to track players
CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- creates a table to track matches
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner INT REFERENCES players (id),
  loser INT REFERENCES players (id)
);

-- returns a view with columns:
--    player id
--    player name
--    total wins that a player has
--    total matches that a player competed in
CREATE OR REPLACE VIEW standings AS
  SELECT players.id,
         players.name,
         SUM(CASE WHEN players.id = matches.winner THEN 1 ELSE 0 END) AS wins,
         COUNT(matches) AS match_count
  FROM players LEFT OUTER JOIN matches
  ON players.id = matches.winner
    OR players.id = matches.loser
  GROUP BY players.id
  ORDER BY wins DESC;
