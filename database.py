"""Small SQLite helper functions for the Smart Typing Tester."""

import sqlite3
from datetime import datetime
from pathlib import Path


def get_connection(database_path: Path) -> sqlite3.Connection:
    """Open SQLite and return rows that can be accessed by column name."""
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path: Path) -> None:
    """Create the tests table the first time the application starts."""
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_time TEXT NOT NULL,
                wpm REAL NOT NULL,
                accuracy REAL NOT NULL,
                errors INTEGER NOT NULL,
                correct_chars INTEGER NOT NULL,
                incorrect_chars INTEGER NOT NULL,
                time_taken INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                paragraph_length TEXT NOT NULL
            )
            """
        )


def save_result(database_path: Path, result: dict) -> int:
    """Insert one completed test and return its new id."""
    date_time = datetime.now().isoformat(timespec="seconds")
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO tests (
                date_time, wpm, accuracy, errors, correct_chars,
                incorrect_chars, time_taken, difficulty, paragraph_length
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date_time,
                result["wpm"],
                result["accuracy"],
                result["errors"],
                result["correct_chars"],
                result["incorrect_chars"],
                result["time_taken"],
                result["difficulty"],
                result["paragraph_length"],
            ),
        )
        return cursor.lastrowid


def get_result(database_path: Path, result_id: int):
    """Find one result by id."""
    with get_connection(database_path) as connection:
        return connection.execute(
            "SELECT * FROM tests WHERE id = ?", (result_id,)
        ).fetchone()


def get_history(database_path: Path):
    """Return the newest tests first."""
    with get_connection(database_path) as connection:
        return connection.execute(
            "SELECT * FROM tests ORDER BY id DESC LIMIT 50"
        ).fetchall()


def get_summary(database_path: Path) -> dict:
    """Return the small set of best-performance values used by the UI."""
    with get_connection(database_path) as connection:
        summary = connection.execute(
            """
            SELECT
                COUNT(*) AS total_tests,
                COALESCE(MAX(wpm), 0) AS best_speed,
                COALESCE(MAX(accuracy), 0) AS best_accuracy,
                COALESCE(MIN(errors), 0) AS lowest_errors
            FROM tests
            """
        ).fetchone()
        return dict(summary)