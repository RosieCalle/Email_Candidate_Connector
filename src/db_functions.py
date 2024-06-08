import psycopg2
import json
import os
import pandas as pd
import logging
from logger_config import setup_logger
# Setup a logger with a custom name and log level
logger = setup_logger('email-candidate')

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
schema1 = db_config['schema']


# Connect to the PostgreSQL server
db_conn = psycopg2.connect(
    dbname=db_name,
    user=pg_user,
    password=pg_pass,
    host=db_host,
    port=db_port
)

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
        statement = f"SELECT EXISTS(SELECT 1 FROM {schema1}.{table_name} WHERE {column_name} = %s);"
        cursor.execute(statement, (value,))
        result = cursor.fetchone()[0]
        logger.debug(f"Checking if {value} exists in {column_name}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to check if {value} exists in {column_name}: {e}")
        db_conn.rollback()
        # Re-raise the exception
        raise

def save_to_database(data_row: dict, table_name):
    """
    Insert data_row to a PostgreSQL table.
    Parameters:
    data_row: dict
    table_name (str): The name of the table to insert to.
    """
    # Get the list of columns from the data_row
    columns = ', '.join(data_row.keys())
    logger.debug(f"Columns: {columns}")

    # Prepare the placeholders for the INSERT statement
    placeholders = ', '.join(['%s'] * len(data_row))
    logger.debug(f"Placeholders: {placeholders}")

    # Prepare the INSERT statement
    insert_statement=f"INSERT INTO {schema1}.{table_name} ({columns}) VALUES ({placeholders});"
    logger.debug(f"Insert statement: {insert_statement}")
    
    # Prepare the data for insertion
    data = tuple(data_row.values())
    logger.debug(f"Data: {data}")
    
    try:
        # Create a cursor object
        cursor = db_conn.cursor()
        
        # Execute the INSERT statement
        cursor.execute(insert_statement, data)
        
        # Commit the transaction
        db_conn.commit()
                
    except Exception as e:
        logger.error(f"Failed to insert row into {schema1}.{table_name}: {e}")
        # An error occurred, roll back the transaction
        db_conn.rollback()

        # Re-raise the exception
        raise

def save_to_attachment(message_id, folder, filename, mimeType):
    table_name = 'attachments'
    data_row = {
        'messageid': message_id,
        'filename': filename,
        'filetype': mimeType,
        'filepath': folder
    }

    logger.debug(f"\n\nData row: {data_row}")

    # Get the list of columns from the data_row
    columns = ', '.join(data_row.keys())
    
    # Prepare the placeholders for the INSERT statement
    placeholders = ', '.join(['%s'] * len(data_row))

    # Prepare the INSERT statement
    insert_statement=f"INSERT INTO {schema1}.{table_name} ({columns}) VALUES ({placeholders});"
    logger.debug(f"Insert statement: {insert_statement}")
    
    # Prepare the data for insertion
    data = tuple(data_row.values())
    
    try:
        # Create a cursor object
        cursor = db_conn.cursor()
        
        # Execute the INSERT statement
        cursor.execute(insert_statement, data)
        
        # Commit the transaction
        db_conn.commit()
                
    except Exception as e:
        logger.error(f"Failed to insert row into {schema1}.{table_name}: {e}")
        db_conn.rollback()
        # An error occurred, roll back the transaction

        # Re-raise the exception
        raise


# # def is_in_blacklist(db_conn, sender_id):
# def is_in_blacklist(sender_id):

#     """
#     Check if a sender_id exists in the blacklist table.

#     Parameters:
#     db_conn (psycopg2.extensions.connection): The database connection.
#     sender_id (int): The sender_id to check.

#     Returns:
#     bool: True if the sender_id exists in the blacklist, False otherwise.
#     """
#     try:
#         cursor = db_conn.cursor()
#         cursor.execute("SELECT EXISTS(SELECT 1 FROM {schema1}.blacklist WHERE senderemail = %s);", (sender_id,))
#         result = cursor.fetchone()[0]
#         return result
#     except Exception as e:
#         print(f"Failed to check if sender_id exists in blacklist: {e}")
#         return False

# def add_to_blacklist(sender_id):

#     """
#     Insert a sender_id into the blacklist table.

#     Parameters:
#     db_conn (psycopg2.extensions.connection): The database connection.
#     sender_id (int): The sender_id to insert into the blacklist.
#     """
#     try:
#         cursor = db_conn.cursor()
#         cursor.execute("INSERT INTO {schema1}.blacklist (senderemail) VALUES (%s);", (sender_id,))
#         db_conn.commit()
#         print(f"Sender_id '{sender_id}' added to blacklist successfully.")
#     except Exception as e:
#         print(f"Failed to add sender_id '{sender_id}' to blacklist: {e}")

