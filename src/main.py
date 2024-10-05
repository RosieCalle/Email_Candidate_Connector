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
# import base64

# not used ?
# import re
# import time
import pickle
import json
# import dateutil.parser as parser
# import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from bs4 import BeautifulSoup
from process_emails import process_email_data
# from db_functions import save_to_attachment_table
# from files import save_body_to_file, convert_html_to_text, save_attachment_to_file
from parser_messages import parsing_message

# import logging
from logger_config import setup_logger
logger = setup_logger('DEBUG',__name__)

# TODO check why is not working
MAX_EMAILS = 1

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
    logger.info("Starting Gmail authentication process...")

    creds = None

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
            logger.warning("New credentials saved to token file.")

    # Log and print token information
    if creds:
        logger.warning(f"Bearer token expires in: {creds.expiry}")

    try:
        service = build('gmail', 'v1', credentials=creds)
        logger.info("Service created successfully.")
        return service 
    except Exception as e:
        logger.error(f"An error occurred during Gmail authentication: {e}")
        return None

def get_messages(service, query, max_messages=2):
    """
    Retrieves messages based on the provided query, up to a maximum number of messages.
    The get_messages() function now handles the `pageToken` correctly and includes error handling to catch any exceptions that occur during the API request.
    Function initializes page_token to None and only includes it in the API request if it has a value. 
    It also includes error handling to catch and print any exceptions that occur during the API request, which can help in diagnosing issues.
    # TODO Add more error handling for the message parsing process.  
    """

    logger.info("Downloading messages...")
    messages = []
    page_token = None
    cont = True
    count = 0 # Initialize count here
    while cont:
        try:
            if page_token:
                result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            else:
                result = service.users().messages().list(userId='me', q=query).execute()
                
            if 'messages' in result:
                messages.extend(result['messages'])
                # Remove 'UNREAD' label from downloaded messages
                for message in result['messages']:
                    service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

            page_token = result.get('nextPageToken', None)
            if not page_token or len(messages) >= max_messages:
                cont = False

            logger.debug (f"Page {count} retrieved")   # for debugging purposes

            count = count + 1

        except Exception as e:
            logger.info(f"An error occurred while downloading messages: {e}")
            break
    
    print("Count in while at get_message:", count)

    logger.info(f"Total message at the inbox: {len(messages)}")
    return messages

def main():
    # Authenticate and Initialize Gmail API Service
    service = gmail_authenticate()
    logger.info(f"Authentication completed successfully.")

    # Read Gmail Inbox, get all new (unread) messages to a local folder
    # Define the query to search for messages
    query = "is:unread" # Example query to search for unread messages
    max_messages=1  # FOR TESTING PURPOSES... Limit the number of messages to retrieve
    # Retrieve messages based on the query
    messages = get_messages(service, query, max_messages)
    logger.info(f"Number of retrieved messages: {len(messages)}")

    # Process each message
    # TODO review why is getting 3 message for 1 message in gmail inbox
    cont = 0
    for message in messages:
        parsing_message(service, message)
        cont = cont + 1
        print("message number:", cont)
    
    logger.info(f"Number of processed messages: {len(messages)}")

if __name__ == '__main__':
    main()

