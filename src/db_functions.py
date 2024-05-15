import psycopg2
import json
import os
import pandas as pd

# TODO add parameters for create or update users

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Define the relative path to the config.json file
relative_config_path = os.path.join(script_dir, '..', 'conf', 'config.json')

config_path = os.path.abspath(relative_config_path)

# Load database parameters from JSON file
with open(config_path, 'r') as file:
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

# TODO move to utils
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

# TODO move to utils
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
        cursor.execute(sqlcmd)
        db_conn.commit()
        print(f"Executed {sqlcmd} ") 
    except Exception as e:
        print(f"Failed to create table: {e}")

def value_exists_in_column(table_name, column_name, value):
    """
    Check if a value exists in a specific column of a table.

    Parameters:
    db_conn (psycopg2.extensions.connection): The database connection.
    table_name (str): The name of the table to search in.
    column_name (str): The name of the column to search in.
    value (str): The value to search for.

    Returns:
    bool: True if the value exists in the column, False otherwise.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column_name} = %s);", (value,))
        result = cursor.fetchone()[0]
        return result
    except Exception as e:
        print(f"Failed to check if value exists in column: {e}")
        return False


# def is_in_blacklist(db_conn, sender_id):
def is_in_blacklist(sender_id):

    """
    Check if a sender_id exists in the blacklist table.

    Parameters:
    db_conn (psycopg2.extensions.connection): The database connection.
    sender_id (int): The sender_id to check.

    Returns:
    bool: True if the sender_id exists in the blacklist, False otherwise.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM blacklist WHERE senderemail = %s);", (sender_id,))
        result = cursor.fetchone()[0]
        return result
    except Exception as e:
        print(f"Failed to check if sender_id exists in blacklist: {e}")
        return False


def add_to_blacklist(sender_id):
    """
    Insert a sender_id into the blacklist table.

    Parameters:
    db_conn (psycopg2.extensions.connection): The database connection.
    sender_id (int): The sender_id to insert into the blacklist.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO blacklist (senderemail) VALUES (%s);", (sender_id,))
        db_conn.commit()
        print(f"Sender_id '{sender_id}' added to blacklist successfully.")
    except Exception as e:
        print(f"Failed to add sender_id '{sender_id}' to blacklist: {e}")
    # finally:
    #     # Close the cursor and connection
    #     cursor.close()
    #     db_conn.close()

def save_to_database(df: pd.DataFrame, table_name: str):
    """
    Append a pandas DataFrame to a PostgreSQL table.

    Parameters:
    df (pd.DataFrame): The DataFrame to append.
    table_name (str): The name of the table to append to.
    """
 # Get the list of columns from the DataFrame
    columns = ', '.join(df.columns)
    
    # Prepare the INSERT statement
    insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES %s;"
    
    # Prepare the data for insertion
    data = [tuple(x) for x in df.to_numpy()]
    
    try:
        # Create a cursor object
        cursor = db_conn.cursor()
        
        # Execute the INSERT statement for each row in the DataFrame
        for row in data:
            cursor.execute(insert_statement, (row,))
        
        # Commit the transaction
        db_conn.commit()
        print(f"Successfully appended {len(df)} rows to table {table_name}.")
    except Exception as e:
        print(f"Failed to append rows to table {table_name}: {e}")
    # finally:
    #     # Close the cursor and connection
    #     cursor.close()
    #     db_conn.close()





