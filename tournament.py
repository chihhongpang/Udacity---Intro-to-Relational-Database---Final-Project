#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM match;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM player;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM player;")
    result = c.fetchone()
    numPlayers = result[0]
    db.close()
    return numPlayers

def registerPlayer(playerName):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      playerName: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO player (name) VALUES (%s);", (playerName,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT p.id, p.name, w.wins, m.matches FROM player AS p, win_count AS w, matches_count AS m WHERE p.id = w.id AND p.id = m.id ORDER BY w.wins DESC;")
    result = c.fetchall()
    db.close()
    return result

def reportMatch(theWinner, theLoser):
    """Records the outcome of a single match between two players.

    Args:
      theWinner:  the id number of the player who won
      theLoser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO match (winner, loser) VALUES (%s, %s);", (theWinner, theLoser,))
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ps = playerStandings()
    result = []
    playerIdIndex = 0
    playerNameIndex = 1
    for i in range(0, len(ps), 2):
        firstPlayer = ps[i]
        secondPlayer = ps[i+1]
        result.append((firstPlayer[playerIdIndex], firstPlayer[playerNameIndex], secondPlayer[playerIdIndex], secondPlayer[playerNameIndex]))
    return result
#registerPlayer('Me')
#deletePlayers()
#countPlayers()
#reportMatch(3,2)
#playerStandings()
swissPairings()