import mysql.connector

from .config import db_config


def get_connection():
    return mysql.connector.connect(**db_config)


def get_players():
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, positions, designation, image_filename, image_url
            FROM players
            WHERE is_active = TRUE
            ORDER BY display_order, id
        """)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_members():
    connection =get_connection()
    cursor=None
    try:
        cursor=connection.cursor(dictionary=True)
        cursor.execute(""" Select id, name, Designation AS designation, image_filename, image_url from
         members where is_active=True Order BY display_order, id  """)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()

            connection.close()


def get_tournaments():
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name, year, description,
                   start_date, end_date, venue, status,
                   cover_image, cover_image_url
            FROM tournaments
            ORDER BY year
        """)

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_tournament(tournament_id):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT *
            FROM tournaments
            WHERE id = %s
        """, (tournament_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_tournament_teams(tournament_id):
    connection = get_connection()
    cursor = None
    try:
        cursor=connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT *
            FROM tournament_teams
            WHERE tournament_id = %s
        """, (tournament_id,))
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_tournament_matches(tournament_id):

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                m.id,
                m.match_date,
                m.match_time,
                m.venue,
                m.stage,
                m.team1_id,
                m.team2_id,
                m.team1_score,
                m.team2_score,
                m.status,

                t1.team_name AS team1_name,
                t2.team_name AS team2_name

            FROM tournament_matches m

            JOIN tournament_teams t1
                ON m.team1_id = t1.id

            JOIN tournament_teams t2
                ON m.team2_id = t2.id

            WHERE m.tournament_id = %s

            ORDER BY m.match_date, m.match_time
        """, (tournament_id,))

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()