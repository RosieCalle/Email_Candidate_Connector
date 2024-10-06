import os
import os.path
import base64
import dateutil.parser as parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from files import save_body_to_file, convert_html_to_text, save_attachment_to_file

from logger_config import setup_logger
logger = setup_logger('INFO',__name__)

def parsing_message(service, message, DATA_FOLDER):
    
    logger.info(f"Processing message {message['id']}...")
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
    headers = msg['payload']['headers']
    parts = msg['payload'].get("parts")

    # Initialize variables to store subject, thread ID, and date/time
    subject = ""
    date_time = ""

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
            logger.debug(f"++++++++++++++++++ part = {part} +++++ mimeType = {mimeType}")

            if mimeType == 'multipart/alternative':
                for subpart in part['parts']:
                    process_part(service, subpart, message, DATA_FOLDER)
            else:
                process_part(service, part, message, DATA_FOLDER)
    else:
        logger.info(f"No parts found in message {message['id']}")

def process_part(service, part, message, DATA_FOLDER):
    mimeType = part['mimeType']
    if 'attachmentId' in part['body']:
        logger.debug(f"------ 3 ----- body:{part['body']}") # DONT REMOVE THIS LINE
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
        save_attachment_to_file(file_data, data_folder, filename, message_id, mimeType)  

    else:
        if mimeType in ['text/plain', 'text/html']:
            logger.debug(f"------ 4 ----- body:{part['body']}") # DONT REMOVE THIS LINE
            data = part['body']['data']
            message_id = message['id']
            thread_id = message['threadId']
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
            msg_body = convert_html_to_text(decoded_data)

            logger.debug(f"         msg_body: {msg_body}")
            
            filename = "body_text_" + thread_id
            data_folder = DATA_FOLDER + "/body"
            save_body_to_file(msg_body, data_folder , filename, message_id)         

