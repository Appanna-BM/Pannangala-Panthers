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
