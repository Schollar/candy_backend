import dbcreds
import mariadb as db


def db_connect():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=dbcreds.user, password=dbcreds.password,
                          host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print('Something is wrong with the DB')
    except:
        print('Something went wrong connecting to the DB')
    return conn, cursor
# Disconnect function that takes in the conn and cursor and attempts to close both


def db_disconnect(conn, cursor):
    try:
        cursor.close()
    except:
        print('Error closing cursor')
    try:
        conn.close()
    except:
        print('Error closing connection')
# Get animal function gets the animal name and description from animals table in DB


def get_posts():
    posts = []
    conn, cursor = db_connect()
    try:
        cursor.execute(
            "SELECT title, content, created_at FROM candy")
        posts = cursor.fetchall()
    except db.OperationalError:
        print('Something is wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    except:
        print('Error with the DB')
    db_disconnect(conn, cursor)

    return posts


def add_post(title, content):
    conn, cursor = db_connect()
    try:
        cursor.execute(
            "INSERT INTO candy (title, content) VALUES (?, ?)", [title, content])
    except db.OperationalError:
        print('Something is wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    conn.commit()
    db_disconnect(conn, cursor)
    return True


def change_post(title, new_title, new_content):
    conn, cursor = db_connect()
    try:
        cursor.execute(
            "UPDATE candy SET title = ?, content = ? WHERE title = ?", [new_title, new_content, title])
    except db.OperationalError:
        print('Something is wrong with the db!')
        return False
    except db.ProgrammingError:
        print('Error running DB query')
    conn.commit()
    db_disconnect(conn, cursor)
    return True


def delete_post(title):
    conn, cursor = db_connect()
    try:
        cursor.execute(
            "DELETE FROM candy WHERE title = ?", [title, ])
    except db.OperationalError:
        print('Something is wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    conn.commit()
    db_disconnect(conn, cursor)
    return True
