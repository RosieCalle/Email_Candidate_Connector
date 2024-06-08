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
import dateutil.parser as parser
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import itables.options as opt
from itables import show
from itables import init_notebook_mode
from bs4 import BeautifulSoup
from process_emails import process_email_data
from db_functions import save_to_attachment
import logging
from logger_config import setup_logger
# Setup a logger with a custom name and log level
logger = setup_logger('email-candidate')


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

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.modify']

###########################################################################################

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

    # global logger # Ensure logger is accessible

    logger.info("Retrieving messages...")
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
                
            page_token = result.get('nextPageToken', None)
            if not page_token or len(messages) >= max_messages:
                cont = False

            logger.debug (f"Page {count} retrieved")   # for debugging purposes

            # if count >= MAX_EMAILS:  # commented out when max_messages argument was added
            #     cont = False  # REMOVE THIS WHEN TESTING IS COMPLETE
            count = count + 1

        except Exception as e:
            logger.error(f"An error occurred while retrieving messages: {e}")
            break

    logger.info(f"Retrieved {len(messages)} messages.")
    return messages


def convert_html_to_text(html_data):
    """
    Converts HTML data to plain text, removing images and HTML formatting.
    NOT USED ANYMORE.  
    """
    soup = BeautifulSoup(html_data, 'html.parser')
    
    # Remove images
    for img in soup.find_all('img'):
        img.decompose()
    
    # Remove HTML formatting
    text = soup.get_text(separator=' ')

    # # Remove extra spaces and newlines, keep just one newline
    # text = re.sub(r'\n+', '\n', text).strip()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove extra newlines
    text = re.sub(r'\n+', '\n', text)
    
    return text

# TODO: make sure that html attachments are saved as html files
# TODO: return value should be value (a boolean) indicating success
# def save_data_to_file(data, folder, file_name):
#     """
#     Saves data to a file.   # NOT USED ANYMORE !!
#     """
#     file_path = os.path.join(folder, file_name)  # data/file
#     try:
#         # dont save the HTML
#         # with open(file_path, 'wb') as file:
#         #     file.write(data)
#         # logger.info(f"Data saved to {file_path}")     
         
#         # Convert HTML to text
#         text = convert_html_to_text(data)   

#         # Save text to a separate file
#         file_name_text = file_name + ".txt"
#         text_file_path = os.path.join(folder, file_name_text)
#         with open(text_file_path, 'w', encoding='utf-8') as text_file:
#             text_file.write(text)
#         # logger.info(f"Text data saved to {text_file_path}")      
#     except Exception as e:
#         print(f"Failed to save data to {file_path}: {e}")


def save_data_to_file(data, folder, filename, message_id, mimeType):
    """
    Saves the given data to a file in the specified folder.
    # message id is added to the filename to make it unique
    # filename is the epoch time in nanoseconds + message id + file extension
    # filetype is determined by the mimeType
    # filepath is the folder 
    """
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save the data to the file
        with open(os.path.join(folder, filename), 'wb') as f:
            f.write(data)
        logger.info(f"Data saved to {folder}/{filename}")

        # try:
        save_to_attachment(message_id, folder, filename, mimeType)
        # except Exception as e:
        #     logger.error(f"Failed to save data to database: {str(e)}")      
        #    
    except Exception as e:
        logger.error(f"Failed to save data to {folder}/{filename}: {str(e)}")



################ BUG ################
def process_message(service, message):
    """
    Processes a single message, extracting its parts and saving them as needed.
    """
    logger.info(f"Processing message {message['id']}...")
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
    headers = msg['payload']['headers']
    parts = msg['payload'].get("parts")

    # Initialize variables to store subject, thread ID, and date/time
    subject = ""
    date_time = ""

    # Extract subject, thread ID, and date/time from headers
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']

        if header['name'] == 'Date':
            date_time = header['value']

        if header['name'] == 'From':
                sender_id = header['value']

            #     # Handle plain text
            #     file_name = f"message_{message['id']}_text.txt"
            #     save_data_to_file(decoded_data, DATA_FOLDER, file_name)
            # elif mimeType in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/rtf']:
            #     # Handle Word documents
            #     file_name = f"message_{message['id']}_word.docx"
            #     save_data_to_file(decoded_data, DATA_FOLDER, file_name)
            # elif mimeType == 'application/pdf':
            #     # Handle PDFs
            #     file_name = f"message_{message['id']}_pdf.pdf"
            #     save_data_to_file(decoded_data, DATA_FOLDER, file_name)
            # elif mimeType in ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']:
            #     # Handle images
            #     file_name = f"message_{message['id']}_image.{mimeType.split('/')[-1]}"
            #     save_data_to_file(decoded_data, DATA_FOLDER, file_name)
            # else:
            #     logger.info(f"Unsupported MIME type for message {message['id']}: {mimeType}")

    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            logger.debug(f"----- mimeType: {mimeType}")

            # TODO where is the attachment name ?
            if 'attachmentId' in part['body']:
                logger.debug(f"--1--- body:{part['body']}") # DONT REMOVE THIS LINE
                if mimeType == 'application/pdf':
                    logger.debug("      found pdf attachment")
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=att_id).execute()
                    data1 = att['data']
                    message_id = message['id']
                    file_data = base64.urlsafe_b64decode(data1)
                    timeid = str(int(time.time_ns())) # epoch time in nanoseconds
                    file_name = timeid + "-" + message_id + ".pdf"
                    logger.debug(f"         file_name: {file_name}")    
                    save_data_to_file(file_data, DATA_FOLDER, file_name, message_id, mimeType)   

            ########### BUG ############
            body = part.get("body")
            partID = part.get("partId") 
         
            logger.debug(f"\n--3--- body:{body}\n") # DONT REMOVE THIS LINE

            # if body and 'data' in body:
            if body.get('data'):
                        
                # Ensure the data is correctly padded
                padding_needed = 4 - (len(body['data']) % 4)
                if padding_needed:
                    padding = '=' * padding_needed
                    padded_data = body['data'] + padding
                else:
                    padded_data = body['data']
                
                try:
                    padded_data = padded_data.replace("-","+").replace("_","/")
                    decoded_data = base64.b64decode(padded_data)

                    # if mimeType and mimeType.startswith('text/'):
                        # This is a text part, likely the message body

                    if partID == "0":                        
                        message_id = message['id']
                        thread_id = message['threadId']
                        msg_body = convert_html_to_text(decoded_data)

                        process_email_data(subject, date_time, sender_id, \
                                        message_id, thread_id, msg_body )
                        
                    # else:
                    #     logger.info(f"Unsupported MIME type for message {message['id']}: {mimeType}")
                except Exception as e:
                    logger.error(f"An error occurred while decoding data for message {message['id']}: {e}")
            else:
                logger.info(f"\nNo body data found for part = {partID} in messageid = {message['id']}")
    else:
        logger.info(f"No parts found in message {message['id']}")







def main():
    # Authenticate and Initialize Gmail API Service
    service = gmail_authenticate()
    logger.info(f"Authentication completed successfully.  The service object is now available for use.")

    # Read Gmail Inbox, get all new (unread) messages to a local folder
    # Define the query to search for messages
    query = "is:unread" # Example query to search for unread messages
    max_messages=1  # FOR TESTING PURPOSES... Limit the number of messages to retrieve
    # Retrieve messages based on the query
    messages = get_messages(service, query, max_messages)
    logger.info(f"Number of retrieved messages: {len(messages)}")

    # Process each message
    # TODO review why is getting 3 message for 1 message in gmail inbox
    for message in messages:
        process_message(service, message)
    
    # print(f"Number of unread messages: {len(messages)}")


if __name__ == '__main__':
    # log_file_path = setup_log_file()
    # logger = configure_logging(log_file_path)

    main()

