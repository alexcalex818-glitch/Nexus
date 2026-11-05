
import sqlite3
import os
from datetime import datetime, timezone


class NexusData:

    def __init__(self, database="nexus.db"):
        self.database = database
        self.initialize()

    def connect(self):
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        with self.connect() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS needs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    country TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            db.execute("""
                CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    location TEXT,
                    source TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            db.execute("""
                CREATE TABLE IF NOT EXISTS outcomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    need_id INTEGER,
                    result TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def save_need(self, category, description, country=""):
        with self.connect() as db:
            cursor = db.execute("""
                INSERT INTO needs
                (category, description, country, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                category,
                description,
                country,
                datetime.now(timezone.utc).isoformat()
            ))
            return cursor.lastrowid

    def save_resource(self, category, description,
                      location="", source=""):
        with self.connect() as db:
            cursor = db.execute("""
                INSERT INTO resources
                (category, description, location, source, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                category,
                description,
                location,
                source,
                datetime.now(timezone.utc).isoformat()
            ))
            return cursor.lastrowid

    def save_outcome(self, need_id, result):
        with self.connect() as db:
            cursor = db.execute("""
                INSERT INTO outcomes
                (need_id, result, created_at)
                VALUES (?, ?, ?)
            """, (
                need_id,
                result,
                datetime.now(timezone.utc).isoformat()
            ))
            return cursor.lastrowid

    def get_needs(self, limit=50):
        with self.connect() as db:
            rows = db.execute("""
                SELECT * FROM needs
                ORDER BY id DESC LIMIT ?
            """, (limit,)).fetchall()

            return [dict(row) for row in rows]

    def get_resources(self, category=None, limit=50):
        with self.connect() as db:
            if category:
                rows = db.execute("""
                    SELECT * FROM resources
                    WHERE category = ?
                    ORDER BY id DESC LIMIT ?
                """, (category, limit)).fetchall()
            else:
                rows = db.execute("""
                    SELECT * FROM resources
                    ORDER BY id DESC LIMIT ?
                """, (limit,)).fetchall()

            return [dict(row) for row in rows]


nexus_data = NexusData()
