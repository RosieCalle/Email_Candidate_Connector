"""
This script is designed to interact with the Gmail API to authenticate a user, retrieve unread messages, and process them. It includes the following functionalities:
1. Gmail Authentication:
    - Checks for existing credentials and refreshes them if necessary.
    - Initiates the OAuth2 flow to obtain new credentials if none are found.
    - Saves new credentials for future use.
    - Logs the expiration time of the credentials.
    - Builds and returns a Gmail service object for API interactions.
2. Message Retrieval:
    - Retrieves messages from the user's mailbox matching a specified query.
    - Removes the 'UNREAD' label from downloaded messages.
    - Continues to fetch messages until a specified maximum number of messages is reached or there are no more messages to fetch.
    - Logs the start of the message download process, page numbers retrieved, any errors that occur, and the total number of messages in the inbox after retrieval.
3. Message Processing:
    - Processes each retrieved message using a specified function.
    - Logs the number of processed emails.
Modules and Libraries:
- os: Provides a way of using operating system dependent functionality.
- pickle: Implements binary protocols for serializing and de-serializing a Python object structure.
- json: Provides an easy way to encode and decode data in JSON format.
- googleapiclient.discovery: Provides a way to build and interact with Google APIs.
- google.oauth2.credentials: Manages OAuth 2.0 credentials.
- google_auth_oauthlib.flow: Handles the OAuth 2.0 Authorization Grant Flow.
- google.auth.transport.requests: Provides a way to refresh credentials.
- process_emails: Custom module to process email data.
- parser_messages: Custom module to parse messages.
- logger_config: Custom module to set up logging configuration.
Constants:
- MAX_EMAILS: The maximum number of emails to process.
- SCOPES: The scopes required for accessing Gmail API.
Functions:
- gmail_authenticate: Authenticates the user with Gmail and returns a service object for interacting with the Gmail API.
- get_messages: Retrieves messages from the user's mailbox matching the specified query.
- main: The main function that orchestrates the authentication, message retrieval, and message processing.
Usage:
- Run the script to authenticate with Gmail, retrieve unread messages, and process them.

"""

import os
import os.path
import pickle
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from process_emails import process_email_data
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
    Authenticates the user with Gmail and returns a service object for interacting with the Gmail API.

    This function performs the following steps:
    1. Checks if a token file exists and loads the credentials from it.
    2. If no valid credentials are found, it initiates the OAuth2 flow to obtain new credentials.
    3. Saves the new credentials to a token file for future use.
    4. Logs the expiration time of the credentials.
    5. Builds and returns a Gmail service object for API interactions.

    Returns:
        googleapiclient.discovery.Resource: A service object for interacting with the Gmail API.
        None: If an error occurs during the authentication process.

    Raises:
        Exception: If an error occurs while building the Gmail service object.
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
    Retrieve messages from the user's mailbox matching the specified query.
    This function downloads messages from the user's mailbox using the provided
    service object and query string. It removes the 'UNREAD' label from the
    downloaded messages and continues to fetch messages until the specified
    maximum number of messages is reached or there are no more messages to fetch.
    Args:
        service (googleapiclient.discovery.Resource): The Gmail API service instance.
        query (str): The query string to filter messages.
        max_messages (int, optional): The maximum number of messages to retrieve. Defaults to 2.
    Returns:
        list: A list of message objects retrieved from the mailbox.
    Raises:
        Exception: If an error occurs while downloading messages.
    Logs:
        Info: Logs the start of the message download process.
        Debug: Logs the page number retrieved during the process.
        Info: Logs any errors that occur during the message download process.
        Info: Logs the total number of messages in the inbox after retrieval.
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
    
    print(f"Unread messages: {count-1}")

    logger.info(f"Total message at the inbox: {len(messages)}")
    return messages

def main():
    # Authenticate and Initialize Gmail API Service
    service = gmail_authenticate()
    logger.info(f"Authentication completed successfully.")

    # Read Gmail Inbox, get all new (unread) messages to a local folder
    # Define the query to search for messages
    query = "is:unread" # Example query to search for unread messages
    
    max_messages=1  # Limit the number of pages of messages to retrieve
    
    # Retrieve messages based on the query
    messages = get_messages(service, query, max_messages)
    logger.info(f"Number of retrieved emailss: {len(messages)}")
    print(f"Number of retrieved emails: {len(messages)}")

    # Process each message
    # TODO review why is getting 3 message for 1 message in gmail inbox
    cont = 0
    for message in messages:
        parsing_message(service, message, DATA_FOLDER)
        cont = cont + 1
        print("message number:", cont)
    
    logger.info(f"Number of processed emails: {cont}")
    print(f"Number of processed emails: {cont}")

if __name__ == '__main__':
    main()

