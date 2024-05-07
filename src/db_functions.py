import psycopg2
import json
# TODO add parameters for create or update users

# Load database parameters from JSON file
with open('db_config.json', 'r') as file:
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
    dbname=db_name,
    user=pg_user,
    password=pg_pass,
    host=db_host,
    port=db_port
)

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

def create_emails_table(db_conn):
    """
    Create the Emails table if it does not already exist.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Emails (
                subject VARCHAR(255),
                timestamp TIMESTAMP,
                messageid VARCHAR(16) PRIMARY KEY,
                threadid VARCHAR(16),
                body TEXT,
                senderid INT
            );
        """)
        db_conn.commit()
        print("Emails table created successfully.")
    except Exception as e:
        print(f"Failed to create Emails table: {e}")


#TODO create fucntion to insert email record





# Example usage
# create_user(db_conn, db_user, db_password)
# update_user_password(db_conn, db_user, db_password)

# Close the connection
db_conn.close()
