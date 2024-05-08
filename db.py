__author__ = "AndyVoyager"

import sqlite3


def read_top_3_scores():
    """
    Connects to the database, retrieves the top 3 scores sorted in descending order,
    and handles exceptions related to SQLite errors.
    Returns a list containing the top 3 scores.
    """
    db = sqlite3.connect("instance/scores.db")
    cursor = db.cursor()

    try:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS scores ("
            "id INTEGER PRIMARY KEY,"
            "score INTEGER)"
        )

        cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 3")
        top_3_scores = cursor.fetchall()

        if len(top_3_scores) < 3:
            for i in range(3 - len(top_3_scores)):
                cursor.execute("INSERT INTO scores (score) VALUES (0)")
            db.commit()

            cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 3")
            top_3_scores = cursor.fetchall()

        return top_3_scores

    except sqlite3.Error as e:
        print("SQLite Error:", e)

    finally:
        db.close()


def add_score(score):
    """
    Inserts a score into the 'scores' table in the SQLite database.

    Parameters:
        score (int): The score to be inserted.

    Returns:
        None

    Raises:
        sqlite3.Error: If there is an error executing the SQL statement.

    Note:
        - The function connects to the 'instance/scores.db' database.
        - The 'scores' table must exist in the database.
        - The score is inserted into the 'score' column of the 'scores' table.
        - The function commits the changes to the database.
        - The database connection is closed in the 'finally' block.
    """
    db = sqlite3.connect("instance/scores.db")
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
        db.commit()

    except sqlite3.Error as e:
        print("SQLite Error:", e)

    finally:
        db.close()
