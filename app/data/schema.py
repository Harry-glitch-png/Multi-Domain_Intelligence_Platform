import sqlite3
# from app.config import DATA_DIR, DB_PATH
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path("DATA") / "intelligence_platform.db"
DATA_DIR = BASE_DIR / "DATA"

def ensure_data_dir():
    """Ensure the DATA directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.
    """
    ensure_data_dir()
    return sqlite3.connect(str(db_path))


def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("✅ Users table created successfully!")


def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    try:
        # cursor.execute("""DROP TABLE IF EXISTS cyber_incidents""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            severity TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT,
            reported_by TEXT
        )
        """)
        conn.commit()
        print("✅ Cyber incidents table created successfully!")
    except Exception as e:
        print("Failed to create cyber_incidents table:", e)
        raise


def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("✅ Datasets metadata table created successfully!")


def create_it_tickets_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("✅ IT tickets table created successfully!")


def create_all_tables(conn):
    """Create all tables."""
    try:
        create_users_table(conn)
        create_cyber_incidents_table(conn)
        create_datasets_metadata_table(conn)
        create_it_tickets_table(conn)
    except Exception as e:
        print("Table creation failed:", e)
        raise


if __name__ == "__main__":
    print("🔍 Initializing database...")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    print(f"✅ Database initialized at: {DB_PATH.resolve()}")
