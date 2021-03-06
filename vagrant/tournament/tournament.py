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
    dbCursor = db.cursor()
    dbCursor.execute("DELETE FROM Matches")
    dbCursor.close()
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    dbCursor = db.cursor()
    dbCursor.execute("DELETE FROM Players;")
    dbCursor.close()
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    dbCursor = db.cursor()
    dbCursor.execute("SELECT COUNT(*) FROM Players")
    result = dbCursor.fetchone()
    dbCursor.close()
    db.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    dbCursor = db.cursor()
    dbCursor.execute("INSERT INTO Players(name) " +
                     " VALUES (%s) RETURNING Id;", (name,))
    dbCursor.close()
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    dbCursor = db.cursor()
    dbCursor.execute(
        "SELECT  p.Id, p.Name" +
        ", (SELECT COUNT(*) FROM Matches m " +
        " WHERE m.WinPlayerId = p.Id) AS Wins  " +
        " , (SELECT COUNT(*) FROM " +
        " Matches m " +
        "  WHERE m.WinPlayerId = p.Id OR m.LosePlayerId = p.Id) " +
        " AS Played" +
        " FROM Players p " +
        " ORDER BY 3 DESC")
    results = dbCursor.fetchall()
    dbCursor.close()
    db.commit()
    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    dbCursor = db.cursor()
    dbCursor.execute("INSERT INTO Matches(WinPlayerId, LosePlayerId) " +
                     " VALUES (%s, %s)", (winner, loser,))
    dbCursor.close()
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
        name2: the second player's name"""
    db = connect()
    dbCursor = db.cursor()
    dbCursor.execute(
        "SELECT p.Id, p.Name," +
        "(SELECT COUNT(*) FROM Matches m " +
        " WHERE m.WinPlayerId = p.Id) " +
        " FROM Players p " +
        " ORDER BY 3 DESC")
    list = dbCursor.fetchall()
    pairings = [
                (list[i-1][0], list[i-1][1], p[0], p[1])
                for i, p in enumerate(list)
                if (i+1) % 2 == 0
               ]
    dbCursor.close()
    db.close()
    return pairings
