import sqlite3

def check():
    conn = sqlite3.connect("chess.db")
    cursor = conn.cursor()
    
    print("--- Users Table ---")
    cursor.execute("SELECT id, google_id, email, name FROM users")
    users = cursor.fetchall()
    for u in users:
        print(u)
        
    print("\n--- Games Table (Players) ---")
    cursor.execute("SELECT id, white_player_id, black_player_id FROM games")
    games = cursor.fetchall()
    for g in games:
        print(g)
        
    conn.close()

if __name__ == "__main__":
    check()

