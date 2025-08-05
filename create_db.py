import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'users' table if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insert sample users
sample_users = [
    ('admin', 'admin123'),
    ('user1', 'pass123'),
    ('alice', 'alicepass'),
    ('bob', 'bobsecure')
]

for user in sample_users:
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", user)
    except sqlite3.IntegrityError:
        # Skip if username already exists
        pass

# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ users.db created with sample users.")

