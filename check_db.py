import sqlite3

def show_users():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        print("📋 Users in database:")
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if conn:
            conn.close()

show_users()

