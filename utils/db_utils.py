# This script is for automate some common tasks with the DB
import os
import json
import psycopg2

# check for the correct folder paths for Windows and Linux
# Read configuration file
script_dir = os.path.dirname(os.path.realpath(__file__))
relative_config_path = os.path.join(script_dir, '..', 'conf', 'config.json')
config_path = os.path.abspath(relative_config_path)
with open(config_path, 'r') as file:
    config = json.load(file)

# Extract database parameters
db_name = config['db_name']
db_user = config['db_user']
db_password = config['db_password']
db_host = config['db_host']
db_port = config['db_port']
pg_user = config['pg_user']
pg_pass = config['pg_pass']

# Connect to the PostgreSQL server
db_conn = psycopg2.connect(
    dbname=db_name, # Connect to the default database
    user=pg_user,    # Use the default user 'postgres'
    password=pg_pass, # Replace with your actual PostgreSQL password for 'postgres' user
    host=db_host,
    port=db_port
)
# db_conn.autocommit = True # Enable autocommit mode

def check_and_create_database(db_conn, db_name):
    """
    Check if the database exists and create it if not.
    """
    try:
        db_cursor = db_conn.cursor()
        db_cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if db_cursor.fetchone() is None:
            db_cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created.")
        else:
            print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Failed to check and create database '{db_name}': {e}")

def create_user(db_conn, username, password):
    """
    Create a new user with the specified username and password.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute(f"CREATE USER {username} WITH PASSWORD '{password}';")
        db_conn.commit()
        print(f"User '{username}' created successfully.")
    except Exception as e:
        print(f"Failed to create user '{username}': {e}")

def update_user_password(db_conn, username, new_password):
    """
    Update the password for the specified user.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute(f"ALTER USER {username} WITH PASSWORD '{new_password}';")
        db_conn.commit()
        print(f"Password for user '{username}' updated successfully.")
    except Exception as e:
        print(f"Failed to update password for user '{username}': {e}")

def execute_sql(sqlcmd):
    """
    Execute the sqlcmd
    """
    try:
        cursor = db_conn.cursor()  
        print("\nsqlcom =", sqlcmd)  
        cursor.execute(sqlcmd)
        db_conn.commit()
        print(f"\nExecuted {sqlcmd} ") 
    except Exception as e:
        print(f"Failed to create table: {e}")

# emails table
#sqlcmd = "CREATE TABLE IF NOT EXISTS  emails (subject VARCHAR(255),timestamp VARCHAR(100), messageid VARCHAR(16) PRIMARY KEY, threadid VARCHAR(16), body TEXT, senderid VARCHAR(100),topic VARCHAR(100) ) ;"
#execute_sql(sqlcmd)

# blacklist table
#sqlcmd = "CREATE TABLE IF NOT EXISTS blacklist (senderemail VARCHAR(70)) ;"
#execute_sql(sqlcmd)

# bademail table
#sqlcmd = "CREATE TABLE IF NOT EXISTS  bademails (subject VARCHAR(255),timestamp VARCHAR(100), messageid VARCHAR(20) PRIMARY KEY, threadid VARCHAR(20), body TEXT, senderid VARCHAR(100),topic VARCHAR(100)) ;"
#execute_sql(sqlcmd)

# Example usage
# create_user(db_conn, db_user, db_password)
# update_user_password(db_conn, db_user, db_password)

#check_and_create_database(db_conn, db_name)


# Close the connection to the default database

db_conn.close()