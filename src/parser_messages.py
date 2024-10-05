import os
import os.path
import base64
import dateutil.parser as parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from files import save_body_to_file, convert_html_to_text, save_attachment_to_file

# TODO 
# this code generate circular import error:
#from main import DATA_FOLDER
# solution move the config values to a new file and import 
# the constant from that new file
DATA_FOLDER = "/hd1/dev/projects/email-candidate/data/"


from logger_config import setup_logger
logger = setup_logger('DEBUG',__name__)


def parsing_message(service, message):
    """
    Parsing a single message, extracting its parts and saving them as needed.
    """
    logger.info(f"Processing message {message['id']}...")
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
    headers = msg['payload']['headers']
    parts = msg['payload'].get("parts")

    # Initialize variables to store subject, thread ID, and date/time
    subject = ""
    date_time = ""

    # Extract subject, thread ID, and date/time from headers
    logger.debug(F"There are  {len(headers)} headers")
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']

        if header['name'] == 'Date':
            date_time = header['value']

        if header['name'] == 'From':
                sender_id = header['value']

    if parts:
        cont = 0
        for part in parts:
            cont = cont + 1
            mimeType = part.get("mimeType")
            logger.debug(f"++++++++++++++++++ 0 +++++++++ mimeType: {mimeType}")

            if not isinstance(part, (str, list, tuple)):
                partx = str(part)
                logger.debug(f"------- 1 --------part: {partx[:300]}")
                
                if mimeType == 'multipart/alternative' :
                    logger.info(f"\n -------- 1 --------- mimeType == multipart")

                    bodyx = part.get("body")  
                    logger.info(f"\n -------- 1 --------- bodyx == {bodyx}")
                    if bodyx:
                        data = bodyx.get("data")
                        logger.info(f"\n -------- 1 --------- data == {data}")

                        # decoded_data = base64.urlsafe_b64decode(data)
                        partID = part.get("partId") 
                        if partID == "0":                        
                            message_id = message['id']
                            thread_id = message['threadId']
                            # msg_body = convert_html_to_text(decoded_data)
                            msg_body = "xxxxxxxx"
                            logger.info(f"\n -------- 1 --------- partID: {partID}")
                            logger.info(f"=========== msg_body: {"msg_body"}")

                            # process_email_data(subject, date_time, sender_id, \
                            #                     message_id, thread_id, msg_body )
                            
                            # save body text to a file in data_folder
                            filename = "body_text_" + thread_id
                            data_folder = DATA_FOLDER + "/body"
                            save_body_to_file(msg_body, data_folder , filename, message_id)         
 

                if mimeType == 'text/plain' or mimeType == 'text/html' :
                    logger.info(f"\n -------- 2 --------- mimeType == 'text/html")

                    bodyx = part.get("body")      
                    if bodyx:
                        data = bodyx.get("data")
                        decoded_data = base64.urlsafe_b64decode(data)
                        partID = part.get("partId") 
                        if partID == "0":                        
                            message_id = message['id']
                            thread_id = message['threadId']
                            msg_body = convert_html_to_text(decoded_data)
                            logger.info(f"\n -------- 2 --------- partID: {partID}")
                            logger.info(f"=========== msg_body: {msg_body}")

                            # process_email_data(subject, date_time, sender_id, \
                            #                     message_id, thread_id, msg_body )
                            
                            # save body text to a file in data_folder
                            filename = "body_text_" + thread_id
                            data_folder = DATA_FOLDER + "/body"
                            save_body_to_file(msg_body, data_folder , filename, message_id)                               
                
            # TODO where is the attachment name ?

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
                # timeid = str(int(time.time_ns())) # epoch time in nanoseconds
                # file_name = timeid + "-" + message_id + "." + doc_type
                logger.debug(f"         file_name: {filename}")    
                save_attachment_to_file(file_data, DATA_FOLDER + "/attach", filename, message_id, mimeType)  

        # ########### BUG ############
        # bodyx = part.get("body")
        # partID = part.get("partId") 
        
        # if bodyx:
        #     data = bodyx.get("data")
        #     # Ensure the data is correctly padded
        #     # padding_needed = 4 - (len(body['data']) % 4)
        #     # if padding_needed:
        #     #     padding = '=' * padding_needed
        #     #     padded_data = body['data'] + padding
        #     # else:
        #     #     padded_data = body['data']
            
        #     try:
        #     #     padded_data = padded_data.replace("-","+").replace("_","/")
        #     #     decoded_data = base64.b64decode(padded_data)

        #         decoded_data = base64.urlsafe_b64decode(data)

        #         # if mimeType and mimeType.startswith('text/'):
        #             # This is a text part, likely the message body

        #         # if partID == "0":                        
        #         #     message_id = message['id']
        #         #     thread_id = message['threadId']
        #         #     msg_body = convert_html_to_text(decoded_data)
        #         #     logger.info(f"\n -------- 3 --------- partID: {partID}")
        #         #     logger.info(f"=========== msg_body: {msg_body}")

        #         #     # process_email_data(subject, date_time, sender_id, \
        #         #     #                     message_id, thread_id, msg_body )
                    
        #         #     # save body text to a file in data_folder
        #         #     filename = "body_text_" + thread_id
        #         #     data_folder = DATA_FOLDER + "/body"
        #         #     save_body_to_file(msg_body, data_folder , filename, message_id)
  
                    
        #         # else:
        #         #     logger.info(f"Unsupported MIME type for message {message['id']}: {mimeType}")
        #     except Exception as e:
        #         logger.error(f"An error occurred while decoding data for message {message['id']}: {e}")
        # else:
        #     logger.info(f"\nNo body data found for part = {partID} in messageid = {message['id']}")
    else:
        logger.info(f"No parts found in message {message['id']}")
    
    print("number of parts:", cont )