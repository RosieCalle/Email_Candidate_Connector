
from datetime import datetime
from email.utils import parseaddr
import pandas as pd
from db_functions import value_exists_in_column, save_to_database
from body_analysis import determine_topic

def mark_as_processed(message_id):
    # Here you would apply a label to mark the message as processed
    # This is a placeholder function
    print("this email should be marked as done\n")
    pass

def extract_email(sender_id):
    name, email = parseaddr(sender_id)
    return email


def filter_email(new_data_row):

    print(" ------- filter_email")

    if new_data_row['messageid'] != new_data_row['threadid']:
        # this email is a thread for some message_id        
        new_data_row['topic'] = "- same -"
        save_to_database(new_data_row, "emails")

    else:
        topic = determine_topic(new_data_row['body'])
        # print(" determine_topic --------", topic)
        new_data_row['topic'] = topic
        if topic != "Uncategorized" and topic != "Spam":
            try:
                save_to_database(new_data_row, "emails")
            except Exception as e:
                print(f"Error processing email data: {e}")  
        else:
            try:
                save_to_database(new_data_row, "bademails")
            except Exception as e:
                print(f"Error processing email data: {e}") 

    # print("end categorization\n\n")


def process_email_data(subject: str, date_time: str, sender_id: str, message_id: str, thread_id: str, message_body: str ):
    """ Analitycs of the email data
        body parsing: look for phone number, linkedin account
        email_rejection: there is not attachemnt and body is not related to a job
        thread_analysis: .... 

    """
 
    try:
        # Remove timezone name if present
        timestamp = date_time.split('(')[0].strip()
    except ValueError as e:
        print(f"Error converting date and time: {e}")
        timestamp = None
       
    sender_id = extract_email(sender_id)
    topic = "uncategorized"
    new_row = {'subject': subject, 'timestamp': date_time, 'messageid': message_id, 'threadid': thread_id, 'body': message_body, 'senderid': sender_id, 'topic': topic}

    senderid_in_db = value_exists_in_column("emails", "senderid", sender_id)
    # senderid_in_bl = is_in_blacklist(sender_id)
    messageid_in_db = value_exists_in_column("emails", "messageid", message_id)

    # print(f"\n\nnew_row = {new_row}\n\n")

    if senderid_in_db :
        # duplicate email
        if messageid_in_db:
            # same messageid, but diff threadid
            if thread_id == message_id:
                print("duplicate email")
                return
            else:
                # new thread from same email address
                # print("new thread from same email address")
                filter_email(new_row) # categorize the email, and save it to the database  

        else:  
            # new subject from same email address
            # print("new subject from same email address")
            filter_email(new_row)
    else:
        # new email address
        # print("new email address")
        filter_email(new_row)

        # TODO
        mark_as_processed(message_id)