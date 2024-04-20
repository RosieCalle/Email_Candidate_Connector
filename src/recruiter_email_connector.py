"""
Updated By: Rosie Calle
Updated on: 2024.04.01 1551h

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

Please replace 'credentials.json' with the path to your actual credentials.json file. Also, please note that you need to allow less secure apps on your Google account to send emails using smtplib. You can do this by going to your Google account settings.

Remember to handle sensitive data, like email addresses and names, securely and in compliance with all 
relevant laws and regulations.

    TODO: Implement the above steps in Python code. 
    TODO: Add drawio diagram packges to the project.
    TODO: ADD LOGGING THROUGHOUT THIS PROJECT.  SUPER IMPORTANT !!! 
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

import logging

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


# Check the operating system
if os.name == 'nt': # 'nt' stands for Windows
    DATA_FOLDER = "..\\data\\"
    TOKEN_PATH = 'C:\\webservices\\gmail_credentials\\token.pickle'
    CREDENTIALS_PATH = 'C:\\webservices\\gmail_credentials\\credentials.json'
    LOG_FILE = 'logs\\app.log'
elif os.name == 'posix': # 'posix' stands for Linux/Unix
    DATA_FOLDER = "../data/"
    TOKEN_PATH = '../../token.pickle'
    CREDENTIALS_PATH ='../../client_secret_desktop-app.json'
    LOG_FILE = 'logs/app.log'
else:
    raise OSError("Unsupported operating system")
 
# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Function to log messages
def log_message(message):
    logging.info(message)

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
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Update the path to the credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)

            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    # Log and print token information
    if creds:
        log_message(f"Bearer token expires in: {creds.expiry}")
        print(f"Bearer token expires in: {creds.expiry}")
        log_message(f"Refresh token: {creds.refresh_token}")
        print(f"Refresh token: {creds.refresh_token}")

    try:
        service = build('gmail', 'v1', credentials=creds)
        log_message("Service created successfully")
        print("Service created successfully")
        return service
    except Exception as e:
        log_message(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None

def get_messages(service, query):
    """
    Retrieves messages based on the provided query.

    The get_messages() function now handles the `pageToken` correctly and includes error handling to catch any exceptions that occur during the API request.
    
    Function initializes page_token to None and only includes it in the API request if it has a value. 
    It also includes error handling to catch and print any exceptions that occur during the API request, which can help in diagnosing issues.
    
    # TODO Add more error handling for the message parsing process.  
    
    """
    log_message("Retrieving messages...")
    messages = []
    page_token = None
    while True:
        try:
            if page_token:
                result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            else:
                result = service.users().messages().list(userId='me', q=query).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
            page_token = result.get('nextPageToken', None)
            if not page_token:
                break
        except Exception as e:
            log_message(f"An error occurred while retrieving messages: {e}")
            break
    log_message(f"Retrieved {len(messages)} messages.")
    return messages

def save_data_to_file(data, folder, file_name):
    """
    Saves data to a file.   
    """
    file_path = os.path.join(folder, file_name)  # data/file
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        print(f"Data saved to {file_path}")      
        # Convert HTML to text
        text = convert_html_to_text(data)   

        # Save text to a separate file
        file_name_text = file_name + ".txt"
        text_file_path = os.path.join(folder, file_name_text)
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        print(f"Text data saved to {text_file_path}")      
    except Exception as e:
        print(f"Failed to save data to {file_path}: {e}")

def convert_html_to_text(html_data):
    """
    Converts HTML data to plain text, removing images and HTML formatting.
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

def process_message(service, message):
    """
    Processes a single message, extracting its parts and saving them as needed.
    """
    log_message(f"Processing message {message['id']}...")
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    headers = msg['payload']['headers']
    parts = msg['payload'].get("parts")

    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            if body and 'data' in body:
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

                    if mimeType and mimeType.startswith('text/'):
                        # This is a text part, likely the message body
                        # print(f"Decoded text part for message {message['id']}")
                        save_data_to_file(decoded_data, DATA_FOLDER, f"message_body_{message['id']}.html")
                    elif mimeType and mimeType.startswith('application/'):                  
                        # This is an attachment
                        print(f"Decoded attachment for message {message['id']}")
                        file_name = f"attachment_{message['id']}_{part.get('filename', 'unknown')}"
                        save_data_to_file(decoded_data, DATA_FOLDER,  file_name)
                except Exception as e:
                    log_message(f"An error occurred while decoding data for message {message['id']}: {e}")
                    print(f"Error decoding data for message {message['id']}: {e}")
            else:
                log_message(f"No body data found for part in message {message['id']}")
                print(f"No body data found for part in message {message['id']}")
    else:
        log_message(f"No parts found in message {message['id']}")
        print(f"No parts found in message {message['id']}")

# def read_message(service, message):
#     """
#     This function takes Gmail API `service` and the `id` of a Gmail email
#     and returns a dictionary with all the parts of the email.
#     """
#     print("Entering read_message() function ... ")       # replace this with formal logging to a time-stamped file
    
#     msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
#     # parts can be the message body, or attachments
#     payload = msg['payload']
#     headers = payload.get("headers")
#     parts = payload.get("parts")
#     data = {}
#     if parts:
#         for part in parts:
#             mimeType = part.get("mimeType")
#             body = part.get("body")
#             data = parse_parts(service, part)
#     return data


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

# TODO MVP v2.x --> add Gmail Folder Batch processing to the code.  This will allow the user to select a folder and process all the emails in that folder

# TODO URGENT Collect all messages into the "email_download_batch" folder, so that 1000s of messages don't stack up in the root folder.  This will make the code more efficient and easier to manage.

# TODO URGENT Make sure the LOG file is properly created and populated with messages. 
# TODO Add "Success" and "Failure" messages at the end of get-message() and process-message() functions. .  
# TODO Uupdate the Mmermaid diagram to include the new functions and the new logging feature.
# TODO Create a Mmermaid diagram to show the function call order of the code, to visualize the code and make it easier to understand.

def main():
    # Step 3: Authenticate and Initialize Gmail API Service
    service = gmail_authenticate()
    print(f"Authentication completed successfully.  The service object is now available for use.")

    # Step 4: Read Gmail Inbox, get all new messages to a local folder
    # Define the query to search for messages
    query = "is:unread" # Example query to search for unread messages

    # Retrieve messages based on the query
    messages = get_messages(service, query)
    log_message(f"Number of unread messages: {len(messages)}")

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
    messages_df.to_json(os.path.join(DATA_FOLDER, f"messages_df_{timestamp}.json"))
    messages_df.to_csv(os.path.join(DATA_FOLDER, f"messages_df_{timestamp}.csv"), index=False)


    # TODO: Save all message bodies and attachments to a timestamped folder
    # This part requires additional logic to handle attachments and save them correctly

    # Step 4c: Display the messages in the itables widget so that the user can page through them and filter them. 
    show(messages_df)

    print(f"Number of unread messages: {len(messages)}")
    print("Messages: ", messages)

    # Step 4d: The user uses check boxes in the itables widget to select individual messages to respond to.  
    
    # Step 4e: From a dropdown list of all available message template types, let the user assign the specific response template to use for each  message selected in STEP 4d.  The code below is missing for the actual implementation of the above steps.  

    # Step 5: For all messages selected in Step 4c, create a list of messages for responses that contain the email_id and email_response_template selected by the user.  There is code below for the actual implementation of the above steps.  This could be implemented in the next version of the code.

    # Conceptual step: User selects messages and chooses a template
    # This step involves user interaction and would require an interactive environment to implement fully

    # messages_reply_list = itables.interactive.show(messages, paging=True, search=True, select='checkbox', select_all='none', showRowNames=True)

    # Step 6: Load Mail Merge Templates corresponding to the email_response_template selected by the user for each message.   The example code immediatley below does not include the functionality to load the specific response templates for each message selected in the previous step.  The code below is a placeholder for the actual implementation of the this feature.  This could be implemented in the next version of the code.

    # Conceptual step (6?): Load and select response templates
    # This step involves user interaction and would require an interactive environment to implement fully
    # template = load_template('template.txt')

    # Step 7: Create Response Using the specific Mail Merge template selected for each message.
    # Conceptual step (7?): Create TEMPLATED responses and review them
    # This step involves user interaction and would require an interactive environment to implement fully

    # Step 8: Review the draft templated responses in the itables widget and before sending them to the Gmail API let the user approve the responses.  If the user approves the responses, then prepare the Gmail API and send the responses to the selected messages.

    # Step 9: Update the messages in the Gmail inbox to mark them as read.  The code below is a placeholder for the actual implementation of the above steps.  It does not include the functionality to mark the messages as read.  This could be implemented in the next version of the code.

    # for msg in messages_reply_list:
    #     data = read_message(service, msg)
    #     first_name = data.split(' ')[0]
    #     response = render_template('template.txt', first_name=first_name)
    #     # Here you would display the response for review and approval
    #     # If approved, send the email
    #     send_email("Subject", response, "recipient@example.com", "your_email@example.com", "your_password")

    # Conceptual step: Mark DRAFT REPLY TEMPLATED messages as read
    # This step involves interacting with the Gmail API and would require the message IDs
    # for msg in messages_reply_list:
    #     service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()

if __name__ == '__main__':
    main()

# TODO REVIEW
# TODO # URGENT STEP 2 --> get message saved into a dataframe once they are successfully parsed. 
# TODO # URGENT STEP 3 --> Add a function to save the message metadata to a dataframe.  This will allow the user to see the message metadata in the itables widget.
# See the data structure HERE --> https://developers.google.com/gmail/api/reference/rest/v1/users.messages#Message 
#                         messages.append({
#                         'id': message['id'],
#                         'threadId': message['threadId'],
#                         'messageTitle': '', # Assuming you have a way to extract this
#                         'senderName': '', # Assuming you have a way to extract this
#                         'messageDateTime': '', # Assuming you have a way to extract this
#                         'body': data
#                     })
