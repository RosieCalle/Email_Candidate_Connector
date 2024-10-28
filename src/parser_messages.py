
"""
This module provides functionality to parse email messages and save their contents to files.
Functions:
    parsing_message(service, message, DATA_FOLDER):
        Parses an email message, extracts its headers and parts, and processes each part accordingly.
        Parameters:
            service (obj): The Gmail API service instance.
            message (dict): The email message to be parsed.
            DATA_FOLDER (str): The folder path where the email contents will be saved.
    process_part(service, part, message, DATA_FOLDER):
        Processes a part of an email message, handling attachments and body content.
        Parameters:
            service (obj): The Gmail API service instance.
            part (dict): The part of the email message to be processed.
            message (dict): The email message containing the part.
            DATA_FOLDER (str): The folder path where the email contents will be saved.
"""

# import os.path
import base64
# import dateutil.parser as parser
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
from files import save_body_to_file, convert_html_to_text, save_attachment_to_file
from process_emails import process_email_data
from db_functions import save_to_attachment_table

from logger_config import setup_logger
logger = setup_logger('INFO',__name__)

def parsing_message(service, message, DATA_FOLDER):
    """
    Parses an email message and processes its parts.
    Args:
        service (googleapiclient.discovery.Resource): The Gmail API service instance.
        message (dict): The email message to be parsed.
        DATA_FOLDER (str): The folder path where data should be stored.
    Returns:
        None
    This function retrieves the full content of an email message using the Gmail API,
    extracts relevant headers such as subject, date/time, and sender ID, and processes
    each part of the message. If the message contains multiple parts, it recursively
    processes each part based on its MIME type.
    """
    
    logger.info(f"Processing message {message['id']}...")
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
    headers = msg['payload']['headers']
    parts = msg['payload'].get("parts")

    # Extract subject, thread ID, and date/time from headers
    logger.debug(f"There are  {len(headers)} headers for message['id']={message['id']}")
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']

        if header['name'] == 'Date':
            date_time = header['value']

        if header['name'] == 'From':
            sender_id = header['value']
            
    if parts:
        for part in parts:
            mimeType = part['mimeType']
            logger.debug(f" part = {part} ---- mimeType = {mimeType}")

            if mimeType == 'multipart/alternative':
                for subpart in part['parts']:
                    process_part(service, subpart, message, DATA_FOLDER, subject, date_time, sender_id)
            else:
                process_part(service, part, message, DATA_FOLDER, subject, date_time, sender_id)
    else:
        logger.info(f"No parts found in message {message['id']}")


def process_part(service, part, message, DATA_FOLDER, subject, date_time, sender_id):
    """
    Processes a part of an email message, handling both attachments and body content.
    Args:
        service (googleapiclient.discovery.Resource): The Gmail API service instance.
        part (dict): The part of the email message to process.
        message (dict): The entire email message.
        DATA_FOLDER (str): The folder path where attachments and body content will be saved.
    Returns:
        None
    """
    
    mimeType = part['mimeType']
    if 'attachmentId' in part['body']:
        logger.debug(f"attachmentId --- body:{part['body']}") # DONT REMOVE THIS LINE
        if mimeType == 'application/pdf':
            logger.debug("      found PDF attachment")
            doc_type = "pdf"                
        elif mimeType in ['application/msword', 
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                          'application/rtf']:
            logger.debug("      found WORD attachment")
            doc_type = "docx" 
        elif mimeType in ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']:
            logger.debug("      found image attachment")
            doc_type = "image"           
                                    
        att_id = part['body']['attachmentId']
        att = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=att_id).execute()
        data1 = att['data']
        message_id = message['id']
        file_data = base64.urlsafe_b64decode(data1)
        
        filename = part.get("filename")
        logger.debug(f"         file_name: {filename}")    
        data_folder = DATA_FOLDER + "/attach"
        
        # save attachments as a file
        save_attachment_to_file(file_data, data_folder, filename, message_id, mimeType)  
        
        # save attachments to the database
        save_to_attachment_table(message_id, data_folder, filename, mimeType)

    else:
        if mimeType in ['text/plain', 'text/html']:
            logger.debug(f"html --- body:{part['body']}") # DONT REMOVE THIS LINE
            data = part['body']['data']
            message_id = message['id']
            thread_id = message['threadId']
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
            msg_body = convert_html_to_text(decoded_data)

            logger.debug(f"         msg_body: {msg_body}")
            
            filename = "body_text_" + thread_id
            data_folder = DATA_FOLDER + "/body"
            
            # save body as a text file
            save_body_to_file(msg_body, data_folder , filename, message_id)       
            
            #filter, select and save the emails data to the database
            process_email_data(subject, date_time, sender_id, message_id, thread_id, msg_body )

