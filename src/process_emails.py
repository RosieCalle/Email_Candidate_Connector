# import pandas as pd
from datetime import datetime
from email.utils import parseaddr
from db_functions import value_exists_in_column, save_to_database
from filter import determine_topic

from logger_config import setup_logger
logger = setup_logger('DEBUG',__name__)

def extract_email(sender_id):
    name, email = parseaddr(sender_id)
    return email

def filter_email(new_data_row):
    """
    Filters and processes an email data row based on its message ID and thread ID.
    This function determines whether the email is part of a thread or a new topic.
    If it is part of a thread, it assigns a default topic and SAVES it to the "emails" table.
    If it is a new topic, it determines the topic from the email body and SAVES it to the
    appropriate table based on the topic classification.
    Args:
        new_data_row (dict): A dictionary containing email data with keys such as 'messageid',
                             'threadid', and 'body'.
    Raises:
        Exception: If there is an error saving the email data to the database, it logs the error.
    """
    
    logger.debug("Started: filter_email")

    if new_data_row['messageid'] != new_data_row['threadid']:
        # this email is a thread for some message_id        
        new_data_row['topic'] = "- same -"
        save_to_database(new_data_row, "emails")
    else:
        topic = determine_topic(new_data_row['body'])
        logger.debug(f"determine_topic : {topic}")
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

