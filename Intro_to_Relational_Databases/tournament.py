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
    dbConnection = connect()
    c = dbConnection.cursor()
    c.execute("DELETE FROM matches")
    dbConnection.commit()
    dbConnection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    dbConnection = connect()
    c = dbConnection.cursor()
    c.execute("DELETE FROM players")
    dbConnection.commit()
    dbConnection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # TODO: Add in the SQL code to count players
    dbConnection = connect()
    c = dbConnection.cursor()
    c.execute("SELECT count(name) FROM players;")
    count = c.fetchone()[0]
    dbConnection.commit()
    dbConnection.close()

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    dbConnection = connect()
    c = dbConnection.cursor()
    c.execute("INSERT INTO players (Name) VALUES (%s)", (name,))
    dbConnection.commit()
    dbConnection.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    dbConnection = connect()
    c = dbConnection.cursor()
    c.execute("INSERT INTO matches (ID, Result) VALUES (%s, %s)", (winner, 'Win'))
    c.execute("INSERT INTO matches (ID, Result) VALUES (%s, %s)", (loser, 'Loss'))
    dbConnection.commit()
    dbConnection.close()


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
    dbConnection = connect()
    c = dbConnection.cursor()

    query = """SELECT Win.ID, Win.Name,
                COALESCE(Win."WinCount", 0),
                COALESCE(Mat."MatchCount", 0)
                FROM
                    (
                    SELECT Pla.ID, Pla.Name,
                    COALESCE(wincount, 0) as "WinCount"
                    FROM Players Pla
                    LEFT JOIN (
                        SELECT Mat.ID, COUNT(Mat.Result) as wincount
                        FROM Matches Mat
                        WHERE Mat.Result = 'Win'
                        GROUP By Mat.ID
                        ) WC
                    ON Pla.ID=WC.ID
                    ) Win
                LEFT JOIN
                    (
                    SELECT Mat.ID,
                    COALESCE(COUNT(Mat.Result), 0) as "MatchCount"
                    FROM Matches Mat
                    GROUP BY Mat.ID
                    ) Mat
                ON Win.ID=Mat.ID
                ORDER By COALESCE(Win."WinCount", 0) Desc;"""

    c.execute(query)
    results = c.fetchall()
    dbConnection.close()
    return results

    '''
    return results
    QUERY = """
        SELECT players.ID as ID, players.Name as Name, sum(COALESCE(matches.result,0)) as Wins, count(matches.result) as Matches
        FROM players
        LEFT JOIN matches
        ON players.ID = matches.ID
        GROUP BY players.id;
    """
    c.execute(QUERY)
    results = c.fetchall()
    dbConnection.close()
    return results
    '''

# TODO: FINISH
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
    '''
    standings = playerStandings()
    lenStandings = (len(standings) / 2)
    i = 0
    pairings = []
    while (i < lenStandings):
        if (lenStandings < 1):
            break
        else:
            pairings.append((standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]))
            i += 1
    return pairings
    '''
    standings = playerStandings()

    pairings = []
    paired = []
    for player in standings:
        # if len < 4, less than 2 players are paired
        # each player has a len of 2 because id and name are used for each player
        if len(paired) < 4:
            paired.append(player[0])
            paired.append(player[1])
        # if len == 4, 2 players are paired
        if len(paired) == 4:
            pairings.append(tuple(paired))
            paired = []

    return pairings
