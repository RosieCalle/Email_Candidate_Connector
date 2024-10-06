# import pandas as pd
from datetime import datetime
from email.utils import parseaddr
from db_functions import value_exists_in_column, save_to_database
from filter import determine_topic

from logger_config import setup_logger
logger = setup_logger('DEBUG',__name__)


def mark_as_processed(message_id):
    # Here you would apply a label to mark the message as processed
    # This is a placeholder function
    print("this email should be marked as done\n")
    pass

def extract_email(sender_id):
    name, email = parseaddr(sender_id)
    return email

def filter_email(new_data_row):

    logger.debug("Started: filter_email")

    if new_data_row['messageid'] != new_data_row['threadid']:
        # this email is a thread for some message_id        
        new_data_row['topic'] = "- same -"
        save_to_database(new_data_row, "emails")

    else:
        topic = determine_topic(new_data_row['body'])
        logger.debug("determine_topic :", topic)
        new_data_row['topic'] = topic
        if topic != "Uncategorized" and topic != "Spam":
            try:
                save_to_database(new_data_row, "emails")
            except Exception as e:
                logger.error(f"Error processing email data for emails table: {e}")  
        else:
            try:
                save_to_database(new_data_row, "bademails")
            except Exception as e:
                logger.error(f"Error processing email data for bademails table: {e}") 

    logger.debug("Ended: filter_email \n\n")


def process_email_data(subject: str, date_time: str, sender_id: str, message_id: str, thread_id: str, message_body: str ):
    """ Analitycs of the email data
        body parsing: look for phone number, linkedin account
        email_rejection: there is not attachemnt and body is not related to a job
        thread_analysis: .... 

    """
 
    # try:
    #     # Remove timezone name if present
    #     timestamp = date_time.split('(')[0].strip()
    # except ValueError as e:
    #     logger.error(f"Error converting date and time: {e}")
    #     timestamp = None
       
    sender_id = extract_email(sender_id)
    topic = "uncategorized"
    new_row = {'subject': subject, 'timestamp': date_time, 'messageid': message_id, 'threadid': thread_id, 'body': message_body, 'senderid': sender_id, 'topic': topic}

    senderid_in_db = value_exists_in_column("emails", "senderid", sender_id)
    messageid_in_db = value_exists_in_column("emails", "messageid", message_id)

    logger.debug(f"\n\nnew_row = {new_row}\n\n")

    if senderid_in_db :
        # duplicate email
        if messageid_in_db:
            # same messageid, but diff threadid
            if thread_id == message_id:
                logger.info("duplicate email")
                return
            else:
                # new thread from same email address
                logger.info("new thread from same email address")
                filter_email(new_row) # categorize the email, and save it to the database  

        else:  
            # new subject from same email address
            logger.info("new subject from same email address")
            filter_email(new_row)
    else:
        # new email address
        logger.info("new email address")
        filter_email(new_row)

        # TODO
        mark_as_processed(message_id)