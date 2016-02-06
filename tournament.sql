-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS player; --Drop table as I revise my schema

CREATE TABLE player (
	id	serial	PRIMARY KEY,
	name	text NOT NULL
);

DROP TABLE IF EXISTS match; -- Drop table as I revise my schema 

CREATE TABLE match (
	id	serial	PRIMARY KEY,
	winner serial	REFERENCES player(id),
	loser	serial	REFERENCES player(id)
);

CREATE VIEW win_count AS SELECT count(m.winner) as wins FROM player as p LEFT JOIN match as m ON p.id = m.winner GROUP BY p.id ORDER BY wins;
CREATE VIEW lose_count AS SELECT count(m.loser) as loses FROM player as p LEFT JOIN match as m ON p.id = m.loser GROUP BY p.id ORDER BY loses;
CREATE VIEW matches_count AS SELECT w.id, (w.wins + l.loses) as matches FROM win_count as w, lose_count as l WHERE w.id = l.id;
