import psycopg2
from psycopg2.extras import DictCursor

# PostgreSQL connection settings
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'service2_db'
DB_USER = 'postgres'
DB_PASSWORD = 'nazih_ali97'

# Connect to the database
conn2 = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create a cursor for executing SQL queries
cur2 = conn2.cursor(cursor_factory=DictCursor)

# Create the firms table
cur2.execute("""
    CREATE TABLE IF NOT EXISTS firms (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL
    )
""")

# Create the auto_markets table
cur2.execute("""
    CREATE TABLE IF NOT EXISTS auto_markets (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        firm_id INTEGER NOT NULL,
        FOREIGN KEY (firm_id) REFERENCES firms (id)
    )
""")

# Create the cars table
cur2.execute("""
    CREATE TABLE IF NOT EXISTS auto (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        number VARCHAR(20) NOT NULL,
        auto_market_id INTEGER NOT NULL,
        FOREIGN KEY (auto_market_id) REFERENCES auto_markets (id)
    )
""")

# Commit the changes to the database
conn2.commit()

# Close the cursor and connection
cur2.close()
conn2.close()