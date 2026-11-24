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

                m.tournament_id,
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


def get_match(match_id):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                m.id,
                m.tournament_id,
                m.match_date,
                m.match_time,
                m.venue,
                m.stage,
                m.team1_id,
                m.team2_id,
                m.team1_score,
                m.team2_score,
                m.team1_penalty,
                m.team2_penalty,
                m.team1_pconverted,
                m.team2_pconverted,
                m.status,

                t1.team_name AS team1_name,
                t2.team_name AS team2_name,

                tr.name AS tournament_name,
                tr.year AS tournament_year

            FROM tournament_matches m

            JOIN tournament_teams t1
                ON m.team1_id = t1.id

            JOIN tournament_teams t2
                ON m.team2_id = t2.id

            JOIN tournaments tr
                ON m.tournament_id = tr.id

            WHERE m.id = %s
        """, (match_id,))

        return cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_match_events(match_id):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                e.id,
                e.match_id,
                e.team_id,
                e.player_name,
                e.event_type,
                e.minute,
                e.notes,
                t.team_name
            FROM match_events e
            JOIN tournament_teams t
                ON e.team_id = t.id
            WHERE e.match_id = %s
            ORDER BY e.id ASC
        """, (match_id,))

        return cursor.fetchall()

    except mysql.connector.Error as err:
        # Fallback if table doesn't exist yet so app doesn't crash
        print(f"Match events query notice: {err}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def add_match_event(match_id, team_id, player_name, event_type, minute=None, notes=None):
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO match_events (match_id, team_id, player_name, event_type, minute, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (match_id, team_id, player_name, event_type, minute or None, notes or None))

        # If it's a goal, auto-sync team score in tournament_matches
        if event_type == 'goal':
            cursor.execute("SELECT team1_id, team2_id FROM tournament_matches WHERE id = %s", (match_id,))
            match_row = cursor.fetchone()
            if match_row:
                team1_id, team2_id = match_row
                cursor.execute("SELECT COUNT(*) FROM match_events WHERE match_id = %s AND team_id = %s AND event_type = 'goal'", (match_id, team1_id))
                t1_score = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM match_events WHERE match_id = %s AND team_id = %s AND event_type = 'goal'", (match_id, team2_id))
                t2_score = cursor.fetchone()[0]
                cursor.execute("UPDATE tournament_matches SET team1_score = %s, team2_score = %s WHERE id = %s", (t1_score, t2_score, match_id))

        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def delete_match_event(event_id, match_id):
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM match_events WHERE id = %s AND match_id = %s", (event_id, match_id))

        # Recalculate scores if goals were modified
        cursor.execute("SELECT team1_id, team2_id FROM tournament_matches WHERE id = %s", (match_id,))
        match_row = cursor.fetchone()
        if match_row:
            team1_id, team2_id = match_row
            cursor.execute("SELECT COUNT(*) FROM match_events WHERE match_id = %s AND team_id = %s AND event_type = 'goal'", (match_id, team1_id))
            t1_score = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM match_events WHERE match_id = %s AND team_id = %s AND event_type = 'goal'", (match_id, team2_id))
            t2_score = cursor.fetchone()[0]
            cursor.execute("UPDATE tournament_matches SET team1_score = %s, team2_score = %s WHERE id = %s", (t1_score, t2_score, match_id))

        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_tournament_team(team_id):
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                t.id,
                t.tournament_id,
                t.team_name,
                tr.name AS tournament_name,
                tr.year AS tournament_year
            FROM tournament_teams t
            JOIN tournaments tr
                ON t.tournament_id = tr.id
            WHERE t.id = %s
        """, (team_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_team_players(team_id):
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, team_id, player_name, jersey_number, position
            FROM tournament_team_players
            WHERE team_id = %s
            ORDER BY jersey_number, player_name
        """, (team_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Team players query notice: {err}")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def add_team_player(team_id, player_name, jersey_number=None, position=None):
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO tournament_team_players (team_id, player_name, jersey_number, position)
            VALUES (%s, %s, %s, %s)
        """, (team_id, player_name, jersey_number or None, position or None))
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def delete_team_player(player_id, team_id):
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM tournament_team_players
            WHERE id = %s AND team_id = %s
        """, (player_id, team_id))
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

