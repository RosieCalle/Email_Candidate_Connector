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
schema1 = config['schema']

print(f"schema = {schema1}")

# Connect to the PostgreSQL server
db_conn = psycopg2.connect(
    dbname=db_name, # Connect to the default database
    user=pg_user,    # Use the default user 'postgres'
    password=pg_pass, # Replace with your actual PostgreSQL password for 'postgres' user
    host=db_host,
    port=db_port
)
# db_conn.autocommit = True # Enable autocommit mode

def create_schema_if_not_exists(db_conn, schema_name = schema1):
    """
    Create the schema if it does not already exist.
    """
    try:
        cursor = db_conn.cursor()
        # query = """
        #     SELECT schema_name
        #     FROM information_schema.schemata
        #     WHERE schema_name = %s;
        # """
        query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        cursor.execute(query)

        # if cursor.fetchone() is None:
        #     query = """
        #         CREATE SCHEMA %s;
        #     """
        #     cursor.execute(query, (schema_name,))

        #     print(f"Schema '{schema_name}' created.")
        # else:
        #     print(f"Schema '{schema_name}' already exists.")
    except Exception as e:
        print(f"Failed to create schema '{schema_name}': {e}")


def create_emails_table(db_conn):
    """
    Create the 'emails' table within the schma schema1.
    """
    try:
        cursor = db_conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS {}.{} (
                subject VARCHAR(255),
                timestamp TIMESTAMP,
                messageid VARCHAR(16) PRIMARY KEY,
                threadid VARCHAR(16),
                body TEXT,
                senderid VARCHAR(100),
                topic VARCHAR(100)
            );
        """.format(schema1, 'emails')
        cursor.execute(query)
        print("Table 'emails' created within 'schema' {schema1}")
        db_conn.commit()
    except Exception as e:
        print(f"Failed to create table 'emails' within 'SCHEMA' {schema1}: {e}")


def create_bademails_table(db_conn):
    """
    Create the 'bademails' table within the 'SCHEMA' schema1.
    """
    try:
        cursor = db_conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS {}.{} (
                subject VARCHAR(255),
                timestamp VARCHAR(100),
                messageid VARCHAR(20) PRIMARY KEY,
                threadid VARCHAR(20),
                body TEXT,
                senderid VARCHAR(100),
                topic VARCHAR(100)
            );
        """.format(schema1, 'bademails')
        cursor.execute(query)
        print("Table 'bademails' created within 'SCHEMA' {schema1}.")
        db_conn.commit()
    except Exception as e:
        print(f"Failed to create table 'bademails' within 'SCHEMA' {schema1}: {e}")


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

def create_attachments_table(db_conn):
    """
    Create the 'attachments' table within the 'SCHEMA' {schema1}.
    """
    try:
        cursor = db_conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS {}.{} (
                messageid VARCHAR(20) PRIMARY KEY,
                filename VARCHAR(20),
                filetype VARCHAR(20),
                filepath VARCHAR(100)
            );
        """.format(schema1, 'attachments')
        cursor.execute(query)
        print("Table 'attachments' created within 'SCHEMA' {schema1}.")
        db_conn.commit()
    except Exception as e:
        print(f"Failed to create table 'attachments' within 'SCHEMA' {schema1}: {e}")


# def create_table(db_conn, schema_name, table_name):
#     """
#     Create a table within the given schema.
#     """
#     try:
#         cursor = db_conn.cursor()
#         query = """
#             CREATE TABLE IF NOT EXISTS {}.{} (
#                 subject VARCHAR(255),
#                 timestamp TIMESTAMP,
#                 messageid VARCHAR(16) PRIMARY KEY,
#                 threadid VARCHAR(16),
#                 body TEXT,
#                 senderid VARCHAR(100)
#             );
#         """.format(schema_name, table_name)
#         cursor.execute(query)
#         db_conn.commit()
#         print(f"Table '{table_name}' in schema '{schema_name}' created.")
#     except Exception as e:
#         print(f"Failed to create table '{table_name}' in schema '{schema_name}': {e}")




if __name__ == "__main__":

    # 1 Create schema
    create_schema_if_not_exists(db_conn)
    # 
    # 2 create emails table
    create_emails_table(db_conn)

    # 3 create table bademails
    create_bademails_table(db_conn)

    # 4 create table attachments
    create_attachments_table(db_conn)


    db_conn.close()



                