"""
Updated By: Rosie Calle
Updated on: 2024.05.14 1555h

This module contains functions to automate the process of reading emails from a Gmail account, 
selecting the first 5 unread messages, and sending personalized responses using a mail merge template.

Functions:
    gmail_authenticate(): Authenticates the user and initializes the Gmail API service.
    search_messages(service, query): Searches for messages in the Gmail inbox based on a query.
    parse_parts(service, parts): Parses the content of an email partition.
    read_message(service, message): Reads a Gmail email and returns a dictionary with all the parts of the email.
    load_template(template_name): Loads a jinja2 template from a file.
    create_response(template, first_name): Creates a personalized response using a jinja2 template.
    main(): The main function that uses the above functions to automate the email reading and response process.

This module requires the following libraries: os, base64, re, time, dateutil.parser, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests, and jinja2.


"""

import os
import os.path
import base64

# not used ?
import re
import time

import pickle
import json

import datetime
import dateutil.parser as parser

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import itables.options as opt
from itables import show
from itables import init_notebook_mode
from bs4 import BeautifulSoup
from process_emails import process_email_data

# TODO check why is not working
MAX_EMAILS = 1

# check for the correct folder paths for Windows and Linux
# Read configuration file
script_dir = os.path.dirname(os.path.realpath(__file__))
relative_config_path = os.path.join(script_dir, '..', 'conf', 'config.json')
config_path = os.path.abspath(relative_config_path)
with open(config_path, 'r') as file:
    config = json.load(file)

if os.name == 'nt': # 'nt' stands for Windows
    DATA_FOLDER = config['win_data_folder']
    TOKEN_PATH = config['win_token_path']
    CREDENTIALS_PATH = config['win_credentials_path']
    LOG_FILE = config['win_log_file']
elif os.name == 'posix': # 'posix' stands for Linux/Unix
    DATA_FOLDER = config['lin_data_folder']
    TOKEN_PATH = config['lin_token_path']
    CREDENTIALS_PATH = config['lin_credentials_path']
    LOG_FILE = config['lin_log_file']
else:
    raise OSError("Unsupported operating system")

# TODO move this code to a logger module
# Create and configure logging
import logging

# TODO move to a module
def setup_log_file():
    """
    Checks if the logs folder and log file exist. If they don't, it creates them.
    """
    # Define the path to the logs folder
    logs_folder_path = os.path.join(os.getcwd(), '../logs')
    # Define the path to the log file
    log_file_path = os.path.join(logs_folder_path, 'app.log')

    # Check if the logs folder exists, if not, create it
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path)

    # Check if the log file exists, if not, create it
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as log_file:
            log_file.write("Log file created.\n")

    return log_file_path

# Configure logging using the paths provided by setup_log_file() function.
def configure_logging(log_file_path):
    global logger
    # print(f"global logger object added in the first line of configure_loggin() function.")
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Create a logger
    logger = logging.getLogger('email_candidate_connector')
    logger.setLevel(logging.INFO)

    # Create a file handler
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

# global logger
# print(f"global logger object added.")

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.modify']

def gmail_authenticate():
    """
    Authenticates the user and initializes the Gmail API service.
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    """
    global logger # Ensure logger is accessible
    logger.info("Starting Gmail authentication process...")

    creds = None

    # # Read the configuration from config.json
    # with open(CREDENTIALS_PATH, 'r') as config_file:
    #     config = json.load(config_file)

    # # Save the credentials for the next run
    # with open(TOKEN_PATH, 'wb') as token:
    #     pickle.dump(creds, token)

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
            logger.info("Credentials loaded from token file.")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logger.info("Credentials refreshed.")
        else:
            # Update the path to the credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            logger.info("New credentials obtained through local server.")

        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
            logger.info("New credentials saved to token file.")

    # Log and print token information
    if creds:
        logger.info(f"Bearer token expires in: {creds.expiry}")
        print(f"Bearer token expires in: {creds.expiry}")  # for debugging purposes
        
        logger.info(f"Refresh token: {creds.refresh_token}")
        print(f"Refresh token: {creds.refresh_token}")  # for debugging purposes

    try:
        service = build('gmail', 'v1', credentials=creds)
        logger.info("Service created successfully.")
        print("Service created successfully")     # for debugging purposes
        return service
    
    except Exception as e:
        logger.info(f"An error occurred during Gmail authentication: {e}")
        print(f"An error occurred: {e}")         # for debugging purposes
        return None

   
def create_response(template, first_name):
    output = template.render(first_name=first_name)
    return output

def load_template(template_name):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)
    return template

def render_template(template_name, **kwargs):
    template = load_template(template_name)
    output = template.render(**kwargs)
    return output

def send_email(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


def main():
    # Step 3: Authenticate and Initialize Gmail API Service
    service = gmail_authenticate()
    print(f"Authentication completed successfully.  The service object is now available for use.")

    # Step 4: Read Gmail Inbox, get all new (unread) messages to a local folder
    # Define the query to search for messages

    query = "is:unread" # Example query to search for unread messages
    max_messages=1  # FOR TESTING PURPOSES... Limit the number of messages to retrieve

    # Retrieve messages based on the query
    messages = get_messages(service, query, max_messages)
    logger.info(f"Number of unread messages: {len(messages)}")

    # Process each message
    for message in messages:
        process_message(service, message)

    # TODO: move to a function
    # Save the stream of all email message IDs to a timestamped file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"message_ids_{timestamp}.json"
    file_path = os.path.join(DATA_FOLDER, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(messages, file)

    # # Step 4b: Create a dataframe to store the messages
    # Convert messages to DataFrame and save to JSON and CSV
    messages_df = pd.DataFrame(messages)
    # messages_df.to_json(os.path.join(DATA_FOLDER, f"messages_df_{timestamp}.json"))
    # messages_df.to_csv(os.path.join(DATA_FOLDER, f"messages_df_{timestamp}.csv"), index=False)
 
    show(messages_df)

    print(f"Number of unread messages: {len(messages)}")


# Call the setup_log_file function during application initialization
if __name__ == '__main__':
    log_file_path = setup_log_file()
    logger = configure_logging(log_file_path)

    main()

