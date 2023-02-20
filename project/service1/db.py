import psycopg2
from psycopg2.extras import DictCursor

# PostgreSQL connection settings
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'service1_db'
DB_USER = 'postgres'
DB_PASSWORD = 'nazih_ali97'

# Connect to the database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create a cursor for executing SQL queries
cursor = conn.cursor(cursor_factory=DictCursor)

# Define the users table schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nickname TEXT NOT NULL,
        date_reg TIMESTAMP DEFAULT NOW()
    );
""")

# Define the cars table schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        number TEXT UNIQUE NOT NULL,
        users_id INTEGER REFERENCES users(id)
    );
""")

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()