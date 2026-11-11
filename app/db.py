"""
DeadlineOS — Database helper (Azure SQL via pyodbc)
Author (Backend): Nishant Kumar

Usage:
    from app.db import get_db, query, execute

    rows = query("SELECT * FROM Announcements WHERE is_active = 1")
    execute("UPDATE StudentTasks SET status = ? WHERE id = ?", ("done", task_id))
"""

import os
import pyodbc
from flask import g, current_app


def get_db():
    """Return a pyodbc connection stored on Flask's application context g."""
    if "db" not in g:
        conn_str = os.getenv("AZURE_SQL_CONN")
        if not conn_str:
            raise RuntimeError("AZURE_SQL_CONN environment variable is not set.")
        g.db = pyodbc.connect(conn_str)
    return g.db


def close_db(e=None):
    """Close the connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, params=()):
    """Run a SELECT and return a list of Row objects."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()


def execute(sql, params=()):
    """Run INSERT / UPDATE / DELETE and commit."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    return cursor.rowcount


def register_teardown(app):
    """Call once from create_app() to auto-close the DB on each request."""
    app.teardown_appcontext(close_db)
