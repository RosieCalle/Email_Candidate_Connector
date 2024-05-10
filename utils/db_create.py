# This script is for the database creation
# (used only once)


import psycopg2
import json

# Load database parameters from JSON file

# TODO fix the relative path
with open('conf/config.json', 'r') as file:
    db_config = json.load(file)

# Extract database parameters
db_name = db_config['db_name']
db_user = db_config['db_user']
db_password = db_config['db_password']
db_host = db_config['db_host']
db_port = db_config['db_port']
pg_user = db_config['pg_user']
pg_pass = db_config['pg_pass']

# Connect to the PostgreSQL server
db_conn = psycopg2.connect(
    dbname="postgres", # Connect to the default database
    user=pg_user,    # Use the default user 'postgres'
    password=pg_pass, # Replace with your actual PostgreSQL password for 'postgres' user
    host=db_host,
    port=db_port
)
db_conn.autocommit = True # Enable autocommit mode
db_cursor = db_conn.cursor()

# Check if the database exists and create it if not
db_cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
if db_cursor.fetchone() is None:
    db_cursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Database '{db_name}' created.")
else:
    print(f"Database '{db_name}' already exists.")

# Close the connection to the default database
db_conn.close()