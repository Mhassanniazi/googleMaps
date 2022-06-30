import mysql.connector


def connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        charset='utf8mb4',
        password="",
        database="storm-proxies1"
    )
    if db.is_connected():
        print("You're connected to database!")
    cursor = db.cursor()
    return cursor, db


def close_connection(cursor, db):

    cursor.close()
    db.close()
    if not db.is_connected():
        print("MySQL connection is closed")
