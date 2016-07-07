#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect(db='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect('dbname=%s' % db)
        cursor = db.cursor()
        return db, cursor
    except:
        raise IOError('Error connecting to database %s' % db)

def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute('DELETE FROM matches')
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute('DELETE FROM players')
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = 'SELECT COUNT(*) AS count FROM players'
    cursor.execute(query)
    count = cursor.fetchone()[0]
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    # can't be too safe with any user inputs, strips any markup
    player = bleach.clean(name, strip=True)
    query = 'INSERT INTO players (name) VALUES (%s)'
    cursor.execute(query, (player,))
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
    db, cursor = connect()
    cursor.execute('SELECT * FROM standings')
    standings = cursor.fetchall()
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = 'INSERT INTO matches (winner, loser) VALUES (%s, %s)'
    cursor.execute(query, (winner, loser,))
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
    db, cursor = connect()
    cursor.execute('SELECT id, name, wins FROM standings ORDER BY wins DESC')
    standings = cursor.fetchall()

    pairings = []
    for i in range(0, len(standings), 2):
        player_id = standings[i][0]
        player_name = standings[i][1]
        oppo_id = standings[i + 1][0]
        oppo_name = standings[i + 1][1]
        pairings.append((player_id, player_name, oppo_id, oppo_name))

    return pairings
