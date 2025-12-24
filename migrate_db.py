import sqlite3
import os

DB_FILE = "chess.db"

def migrate():
    if not os.path.exists(DB_FILE):
        print(f"{DB_FILE} not found. Nothing to migrate.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(games)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "white_player_id" not in columns:
            print("Adding white_player_id column...")
            cursor.execute("ALTER TABLE games ADD COLUMN white_player_id INTEGER REFERENCES users(id)")
        
        if "black_player_id" not in columns:
            print("Adding black_player_id column...")
            cursor.execute("ALTER TABLE games ADD COLUMN black_player_id INTEGER REFERENCES users(id)")
            
        conn.commit()
        print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
