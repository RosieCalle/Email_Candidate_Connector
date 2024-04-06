"""
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

This module requires the following libraries: os, base64, re, time, dateutil.parser, googleapiclient.discovery, 
google_auth_oauthlib.flow, google.auth.transport.requests, and jinja2.

Please replace 'credentials.json' with the path to your actual credentials.json file. Also, please note that you need 
to allow less secure apps on your Google account to send emails using smtplib. You can do this by going to your Google 
account settings.

This is a basic implementation. Depending on your needs, you might want to add error handling, logging, more personalized 
emails, etc. Also, remember to handle sensitive data, like email addresses and names, securely and in compliance with all 
relevant laws and regulations.

## Bing

Sure, I can help you with that. Here's the updated workflow:
- Setup Python Environment
    - Install Python
    - Setup virtual environment
    - Install necessary libraries (Google Client Library for Gmail API, pandas for data handling, jinja2 for templating)
- Authorize Application to Use Gmail
    - Create a project on Google Cloud Console
    - Enable Gmail API
    - Download the credentials.json file
    - Use the credentials.json file to authorize the application
- Authenticate and Initialize Gmail API Service
    - Authenticate using the credentials.json file
    - Initialize the Gmail API service
- Read Gmail Inbox
    - Use the Gmail API service to read the inbox
    - Download new messages to a local folder
- Select First 5 New Messages
    - Filter the messages to get only the new ones
    - Select the first 5 new messages
- Load Mail Merge Template
    - Load a jinja2 template from a file
- Create Response Using Mail Merge
    - Create a function to generate personalized responses for each message using the jinja2 template
    - Send the responses

    TODO: Implement the above steps in Python code. 
    TODO: Add drawio diagram packges to the project.
"""


import os
import os.path
import base64
import re
import time
import pickle
import dateutil.parser as parser
import pandas as pd
import itables.interactive
import itables.options as opt
from itables import show
from itables import init_notebook_mode

# Enable the itables widget in Jupyter Notebook
init_notebook_mode(all_interactive=True)
# TODO: create a startup "run" script to run the Jupyter Notebook server and intialize the itables widget.

from jinja2 import Environment, FileSystemLoader
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# from google.cloud import secretmanager

# def access_secret_version(project_id, secret_id, version_id):
#     """
#     Access the payload for a given secret version.

#     Args:
#         project_id (str): Google Cloud project ID (e.g. 'my-project').
#         secret_id (str): ID of your secret (e.g. 'my-secret').
#         version_id (str): Version of your secret (e.g. 'latest').

#     Returns:
#         str: Decrypted payload of the secret version.
#     """
#     # Create the Secret Manager client.
#     client = secretmanager.SecretManagerServiceClient()

#     # Build the resource name of the secret version.
#     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

#     # Access the secret version.
#     response = client.access_secret_version(request={"name": name})

#     # Return the decoded payload.
#     return response.payload.data.decode('UTF-8')


# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.modify']


# def load_credentials():
#     """
#     Load the path to the credentials file.

#     Returns:
#         str: The path to the credentials file.
#     """
#     credentials_path = os.path.join("c:\\webservices\\", "credentials.json")
#     return credentials_path

# def gmail_authenticate():
#     """Shows basic usage of the Gmail API.
#     Lists the user's Gmail labels.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.

#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)

#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     try:
#         service = build('gmail', 'v1', credentials=creds)
#         print("Service created successfully")
#         return service
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

import os
import base64
import re
import time
import pickle
import dateutil.parser as parser
from jinja2 import Environment, FileSystemLoader
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.modify']

def gmail_authenticate():
    """
    Shows basic usage of the Gmail API.  Lists the user's Gmail labels.
    
    CODE GENERATED BY PHIND AT 2024.04.01 1551h.

    """
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Update the path to the credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file('c:\\webservices\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        print("Service created successfully")
        return service
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def parse_parts(service, parts):
    """
    Utility function that parses the content of an email partition
    """
    data = parts['body']['data']
    data = data.replace("-","+").replace("_","/")
    decoded_data = base64.b64decode(data)
    return decoded_data.decode()

def read_message(service, message):
    """
    This function takes Gmail API `service` and the `id` of a Gmail email
    and returns a dictionary with all the parts of the email.
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    data = {}
    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = parse_parts(service, part)
    return data

def load_template(template_name):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)
    return template

def create_response(template, first_name):
    output = template.render(first_name=first_name)
    return output

def main():
    # Step 1: Setup Python Environment
    # This is done manually

    # Step 2: Authorize Application to Use Gmail
    # This is done manually

    # Step 3: Authenticate and Initialize Gmail API Service
    service = gmail_authenticate()

    # Step 4: Read Gmail Inbox, download all new messages to a local folder
    messages = search_messages(service, "is:unread")

    # Step 4b: Create a dataframe to store the messages

    # Step 4c: Display the messages in the itables widget so that the user can page through them and filter them, and then use check boxes to select individual messges to respond to.  From a dropdown list of all availabe message template types, let the user select the specific response template to use for an indvidual message. 

    # Step 5: For all messages selected in Step 4c, create a list of messages for responses that contain the email_id and email_response_template selected by the user.  The code below is a placeholder for the actual implementation of the above steps.  It does not include the functionality to select the specific response template for each message.  This could be implemented in the next version of the code, OR it could be implemented in the recruiter_email_v3.py version if Phind has the generative capacity.

    messages_reply_list = itables.interactive.show(messages, paging=True, search=True, select='checkbox', select_all='none', showRowNames=True)

    # Step 6: Load Mail Merge Templates corresponding to the email_response_template selected by the user for each message.   The example code immediatley below does not include the functionality to load the specific response templates for each message selected in the previous step.  The code below is a placeholder for the actual implementation of the this feature.  This could be implemented in the next version of the code, OR it could be implemented in the recruiter_email_v3.py version if Phind has the generative capacity.
    template = load_template('template.txt')

    # Step 7: Create Response Using the specific Mail Merge template selected for each message.

    # Step 8: Review the draft templated responses in the itables widget and before sending them to the Gmail API let the user approve the responses.  If the user approves the responses, then prepare the Gmail API and send the responses to the selected messages.

    # Step 9: Update the messages in the Gmail inbox to mark them as read.


    for msg in messages_reply_list:
        data = read_message(service, msg)
        # Here you can do something with the data (like sending a response)
        first_name = data.split(' ')[0]
        response = create_response(template, first_name)
        print(response)

if __name__ == '__main__':
    main()
