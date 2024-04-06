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
    TODO: ADD LOGGING TO THIS PROJECT.  SUPER IMPORTANT !!! 
"""


import os
import os.path
import base64
import re
import time
import pickle
import dateutil.parser as parser
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# itables imports
#import itables.interactive  # deprecated in favor of the line below  
from itables import init_notebook_mode
import itables.options as opt
from itables import show
from itables import init_notebook_mode

# Enable the itables widget in Jupyter Notebook
init_notebook_mode(all_interactive=True)
# TODO: create a startup "run" script to run the Jupyter Notebook server and intialize the itables widget.


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

# The following three functions are not being used yet to create the dataframe container for all email messages.  
# This needs to be implemented in the next version of the code.  
# The code below is an example of placeholder for the actual implementation of the above steps that was created earlier.  

# def search_messages(service, query):
#     print("Entering search_messages() ... Searching for messages...")       # replace this with formal logging to a time-stamped file
#     result = service.users().messages().list(userId='me',q=query).execute()
#     messages = []
#     if 'messages' in result:
#         messages.extend(result['messages'])
#     while 'nextPageToken' in result:
#         page_token = result['nextPageToken']
#         result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
#         if 'messages' in result:
#             messages.extend(result['messages'])
#     return messages


# The error message you're encountering, `HttpError 400 when requesting https://gmail.googleapis.com/gmail/v1/users/me/messages?q=is%3Aunread&pageToken=06861154300024659797&alt=json returned "Precondition check failed."`, typically indicates an issue with the request being made to the Gmail API. The "Precondition check failed" error can occur for several reasons, but in the context of your script, it's likely related to how the `pageToken` is being handled in the `search_messages` function.

# The `pageToken` is used to retrieve the next page of results when there are more messages than can be returned in a single response. The error suggests that the `pageToken` being used is not valid for the request being made. This could happen if the token has expired or if there's an issue with how the token is being passed to the API request.

# To address this issue, let's refine the `search_messages` function to ensure it correctly handles the `pageToken`. Here's an updated version of the function:

def search_messages(service, query):
    """
    Function initializes page_token to None and only includes it in the API request if it has a value. It also includes error handling to catch and print any exceptions that occur during the API request, which can help in diagnosing issues.
    """
    messages = []
    page_token = None
    while True:
        try:
            if page_token:
                result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            else:
                result = service.users().messages().list(userId='me', q=query).execute()
            messages.extend(result.get('messages', []))
            page_token = result.get('nextPageToken', None)
            if not page_token:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return messages

def parse_parts(service, parts):
    """
    Utility function that parses the content of an email partition
    """
    print("Entering parse_parts() ... ")       # replace this with formal logging to a time-stamped file
    data = parts['body']['data']
    data = data.replace("-","+").replace("_","/")
    decoded_data = base64.b64decode(data)
    return decoded_data.decode()

def read_message(service, message):
    """
    This function takes Gmail API `service` and the `id` of a Gmail email
    and returns a dictionary with all the parts of the email.
    """
    print("Entering read_message() function ... ")       # replace this with formal logging to a time-stamped file
    
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
# TODO: add a progress bar to show the progress of the email message downloading process.  
# Implement in the next version of the code.

def load_downloaded_message_ids():
    # Load the list of downloaded message IDs from a file
    try:
        with open('downloaded_message_ids.txt', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# # Message Processing  # Commented out because it is replaced by the full implementation of the function below.
# def process_message(service, message):
#     # Placeholder for processing a message
#     email_content = "Email content here"
#     attachments = ["Attachment data here"]
#     return email_content, attachments


def process_message(service, message):
    """
    Processes a single message by extracting its content and attachments,
    and saves them to a folder named email_batch_download_{timestamp}.
    """
    # Extract the email content
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    email_content = ""

    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = part.get("data")
            if part.get("filename"):
                # This part is an attachment
                file_data = base64.urlsafe_b64decode(data.encode('ASCII'))
                file_path = os.path.join('email_batch_download', f"{message['id']}_{part.get('filename')}")
                with open(file_path, 'wb') as f:
                    f.write(file_data)
            else:
                # This part is the email body
                email_content += parse_parts(service, part)

    # Create a time-stamped folder for this batch of emails
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_path = os.path.join('email_batch_download', timestamp)
    os.makedirs(folder_path, exist_ok=True)

    #TODO: email_batch_download or email_download_batch?  Make sure the folder name is consistent throughout the code.
    
    # Save the email content to a text file
    email_path = os.path.join(folder_path, f"{message['id']}_email_content.txt")
    with open(email_path, 'w') as file:
        file.write(email_content)

    return email_content, folder_path

def parse_parts(service, part):
    """
    Utility function that parses the content of an email partition
    """
    data = part.get("body").get("data")
    if data:
        data = data.replace("-", "+").replace("_", "/")
        decoded_data = base64.b64decode(data)
        return decoded_data.decode()
    else:
        return ""


# Saving Messages and Attachments
# def save_emails_and_attachments(emails, attachments):

#     # Create a time-stamped folder for this batch of emails
#     timestamp = time.strftime("%Y%m%d-%H%M%S")
#     folder_path = os.path.join('email_download_batch', timestamp)
#     os.makedirs(folder_path, exist_ok=True)

#     # Save each email to a text file
#     for i, email in enumerate(emails):
#         email_path = os.path.join(folder_path, f'email_{i}.txt')
#         with open(email_path, 'w') as file:
#             file.write(email)

#     # Save each attachment to its own file
#     for i, attachment in enumerate(attachments):
#         attachment_path = os.path.join(folder_path, f'attachment_{i}')
#         with open(attachment_path, 'wb') as file:
#             file.write(attachment)


def save_emails_and_attachments(emails, attachments):
    # Create a time-stamped folder for this batch of emails
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_path = os.path.join('email_download_batch', timestamp)
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating folder for this batch of emails: {e}")
        return

    # Save each email to a text file
    for i, email in enumerate(emails):
        email_path = os.path.join(folder_path, f'email_{i}.txt')
        try:
            with open(email_path, 'w') as file:
                file.write(email)
            print(f"Saved email to {email_path}")
        except Exception as e:
            print(f"Error saving email to {email_path}: {e}")

    # Save each attachment to its own file

    # Inside the save_emails_and_attachments function, when saving each attachment
    for i, attachment in enumerate(attachments):
        attachment_path = os.path.join(folder_path, f'attachment_{i}')
        try:
            # Check if the attachment is a string and needs to be converted to bytes
            if isinstance(attachment, str):
                # Assuming the attachment is base64-encoded, decode it to bytes
                attachment_bytes = base64.b64decode(attachment)
            else:
                # If the attachment is already bytes, use it as is
                attachment_bytes = attachment

            with open(attachment_path, 'wb') as file:
                file.write(attachment_bytes)
            print(f"Saved attachment to {attachment_path}")
        except Exception as e:
            print(f"Error saving attachment to {attachment_path}: {e}")


def save_downloaded_message_ids(message_ids, folder_path):
    # Save the list of downloaded message IDs to a file within the same timestamped folder
    # save the downloaded_message_ids.txt file with the same batch_id timestamp, 
    # you can modify the save_downloaded_message_ids function to accept an additional parameter
    # for the folder path. Create the downloaded_message_ids.txt file within the same timestamped folder.
    ids_file_path = os.path.join(folder_path, 'downloaded_message_ids.txt')
    with open(ids_file_path, 'w') as file:
        for msg_id in message_ids:
            file.write(f"{msg_id}\n")

# TODO: Add docstrings to all functions, instead of just inline comments.
# TODO: reorder the functions in the order they are called in the main function.
# TODO: The email template files were renamed to include the word "TEMPLATE" in the name. 
# TODO:     Rename the email templates so the program references the correct template for each email message.


# Utility Functions
# TODO: Move all utility functions here. 

def main():
    # Step 1: Setup Python Environment
    # This is done manually

    print("Step 1: Starting the email processing script...")

    # Step 2: Authorize Application to Use Gmail
    # This is done manually
    print("Step 2: Authorize Application to Use Gmail...")

    # Step 3: Authenticate 
    # Initialize the Gmail API service
    service = gmail_authenticate()
    print(f"Step 3: Authentication completed successfully.  The service object is now available for use.")

    # Step 4: Read Gmail Inbox, download all new messages to a local folder
    # Load the list of already downloaded message IDs
    downloaded_message_ids = load_downloaded_message_ids()
    print("Step 4a: Loaded list of downloaded message IDs.")

    # Search for unread messages
    messages = search_messages(service, "is:unread")
    print(f"Step 4b: Found {len(messages)} unread messages.")
    print("Messages: ", messages)


    # Filter out messages that have already been downloaded
    new_messages = [msg for msg in messages if msg['id'] not in downloaded_message_ids]
    print(f"Step 4c: {len(new_messages)} new messages will be processed.")

    # Create a time-stamped folder for this batch of emails
    # Create the email_download_batch folder immediately
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_path = os.path.join('email_download_batch', timestamp)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Created folder for this batch of emails: {folder_path}")


    # Process and download new messages
    for msg in new_messages:
        # Process the message (e.g., extract content and attachments)
        email_content, attachments = process_message(service, msg)

        # Save the email and attachments
        save_emails_and_attachments([email_content], attachments)
        print(f"Saved email and attachments for message ID: {msg['id']}")

        # Add the message ID to the list of downloaded message IDs
        downloaded_message_ids.append(msg['id'])

        # save_downloaded_message_ids(downloaded_message_ids)
        # After creating the timestamped batch folder_path, save the downloaded message IDs to a file within that folder.
        save_downloaded_message_ids(downloaded_message_ids, folder_path)
        print(f"Updated list of downloaded message IDs.")


    # Step 4a: Save emails and attachments to a local folder

    # Step 4b: Create a dataframe to store the messages
    messages_df = pd.DataFrame(messages)

    # Step 4c: Display the messages in the itables widget so that the user can page through them and filter them. 
    show(messages_df)

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


# Ensure this line is at the end of your file, before the if __name__ == '__main__': line
if __name__ == '__main__':
    main()

