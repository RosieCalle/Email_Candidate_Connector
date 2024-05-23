
from datetime import datetime
from email.utils import parsedate_to_datetime, parseaddr
import pandas as pd
from db_functions import value_exists_in_column, add_to_blacklist, is_in_blacklist, save_to_database
from body_analysis import determine_topic

def mark_as_processed(message_id):
    # Here you would apply a label to mark the message as processed
    # This is a placeholder function
    print("this email should be marked as done\n")
    pass

def extract_email(sender_id):
    name, email = parseaddr(sender_id)
    return email

def process_email_data(subject: str, date_time: str, sender_id: str, message_id: str, thread_id: str, message_body: str ):
    """ Analitycs of the email data
        body parsing: look for phone number, linkedin account
        email_rejection: there is not attachemnt and body is not related to a job
        thread_analysis: .... 

    """
    df_email = pd.DataFrame(columns=['subject', 'timestamp', 'messageid', 'threadid', 'body', 'senderid', 'topic'])
    try:
        # Remove timezone name if present
        timestamp = date_time.split('(')[0].strip()

        # TODO make compatible with postgress timestamp
        # # Parse the date
        # date = parsedate_to_datetime(date_string)
        # # Format the date
        # timestamp = date.strftime('%Y-%m-%d %H:%M:%S')

    except ValueError as e:
        print(f"Error converting date and time: {e}")
        timestamp = None
    
    sender_id = extract_email(sender_id)

    # print("====== process_emails.py ======")
    # print(f"\n\nSubject: {subject}")
    # print(f"Date/Time: {timestamp}")
    # print(f"Sender ID: {sender_id}")
    # print(f"Message ID: {message_id}")
    # print(f"Thread ID: {thread_id}")
    # print(f"Message Body: {message_body[:200]}")

    topic = "uncategorized"
    new_row = {'subject': subject, 'timestamp': date_time, 'messageid': message_id, 'threadid': thread_id, 'body': message_body[:200], 'senderid': sender_id, 'topic': topic}

    if not value_exists_in_column("emails", "senderid", sender_id): # sender_id is not in the table "emails"
        # if not is_in_blacklist(sender_id):           
        topic = determine_topic(message_body)
        print("\n - determine_topic -", topic)
        if topic is not None:
            try:
                new_row['topic'] = topic
                df_email = df_email._append(new_row, ignore_index=True)
                save_to_database(df_email, "emails")
            except Exception as e:
                print(f"Error processing email data: {e}")
        else:   
            # logger.info(f"message_body is not good. message_id: {message_id}")
            print(f"message_body is not good. message_id: {message_id}")
            # add_to_blacklist(sender_id)
            new_row['topic'] = topic
            df_email = df_email._append(new_row, ignore_index=True)
            save_to_database(df_email, "bademails")
        # else:
        #     # logger.info(f"message_body is not good. message_id: {message_id}")
        #     print(f"sender in the blacklist: message_id: {message_id}")
        #     new_row['topic'] = "blacklist"
        #     df_email = df_email._append(new_row, ignore_index=True)
        #     save_to_database(df_email, "bademails")
    else: # it is a new message from a known sender_id
        if message_id == thread_id: # new email from same sender_id, with meesage_id == thread_id
            if not value_exists_in_column("emails", "messageid", message_id): # avoid duplication
                topic = determine_topic(message_body)
                print("\n - determine_topic -", topic)
                if topic is not None:
                    try:
                        new_row['topic'] = topic
                        df_email = df_email._append(new_row, ignore_index=True)
                        save_to_database(df_email, "emails")
                    except Exception as e:
                        print(f"Error processing email data: {e}")
                else:   
                    # logger.info(f"message_body is not good. message_id: {message_id}")
                    print(f"message_body is not good. message_id: {message_id}")
                    new_row['topic'] = topic
                    df_email = df_email._append(new_row, ignore_index=True)
                    # add_to_blacklist(sender_id)
                    save_to_database(df_email, "bademails")
            else:
                print(f"Email already processed: {message_id}") 
        else: #the email is a thread
            if not value_exists_in_column("emails", "messageid", message_id):
                try:
                    new_row['topic'] = "-same-" # keep the topic unchanged
                    df_email = df_email._append(new_row, ignore_index=True)
                    save_to_database(df_email, "emails")
                except Exception as e:
                    print(f"Error saving email to database: {e}")

        mark_as_processed(message_id)