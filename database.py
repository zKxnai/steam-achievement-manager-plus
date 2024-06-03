import sqlite3

# Define the database file
DB_FILE = "data.db"

def create_tables():
    """Create the tables in the database if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS default_theme (
        id INTEGER PRIMARY KEY,
        theme TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_default_theme(theme):
    """Save the default theme to the database."""
    create_tables()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Clear existing default theme
    cursor.execute("DELETE FROM default_theme")

    # Insert new default theme
    cursor.execute("""
    INSERT INTO default_theme (theme)
    VALUES (?)
    """, (theme,))

    conn.commit()
    conn.close()

def load_default_theme():
    """Retrieve the default theme from the database. If no theme is found, set it to 'Dark'."""
    create_tables()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT theme FROM default_theme")
    theme_row = cursor.fetchone()

    if theme_row:
        theme = theme_row[0]
    else:
        # If no theme is found, set it to 'Dark' and save it to the database
        theme = "Dark"
        save_default_theme(theme)

    conn.close()

    return theme

