# Python example with psycopg2
import os
import psycopg2
""" Script to connect to the [Neon] database with some testing of the connection with a query. Still unclear if we will use Neon or Supabase"""



# Load the environment variable
database_url = os.getenv('DATABASE_URL')

# Connect to the PostgreSQL database
conn = psycopg2.connect(database_url)

with conn.cursor() as cur:
    cur.execute("SELECT version()")  # Asks the PostgreSQL Neon Database for its Version
    print(cur.fetchone())  # Fetches the result of the query and prints it as a tuple (containing the version text)

# Close the connection
conn.close()