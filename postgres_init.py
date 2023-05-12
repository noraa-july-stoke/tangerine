import psycopg2

# Establish a connection to the database
conn = psycopg2.connect("postgresql://postgres:C4melz!!@localhost:5432/local_development")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create schema if it's not there
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS tangerine;
""")

# Execute a command: this creates a new table named 'users'
cur.execute("""
    CREATE TABLE IF NOT EXISTS tangerine.users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
""")

# Commit the transaction
conn.commit()

# Close the connection
cur.close()
conn.close()
