
from datetime import datetime
from email.utils import parsedate_to_datetime, parseaddr
import pandas as pd
from db_functions import value_exists_in_column, add_to_blacklist, is_in_blacklist, save_to_database

def mark_as_processed(message_id):
    # Here you would apply a label to mark the message as processed
    # This is a placeholder function
    print("this email should be marked as readed")
    pass

def determine_topic(text_body: str):
    # List of keywords for each topic
    job_offer_keywords = ["job alert", "job offer", "hiring", "vacancy", "open position"]
    job_interest_keywords = ["job search", "looking for a job", "career change"]
    person_looking_keywords = ["job hunting", "applying for jobs", "resume"]
    company_looking_keywords = ["recruiting", "talent acquisition", "hiring team"]

    # # Read the file
    # with open(file_path, 'r') as file:
    #     content = file.read().lower()  # Convert to lowercase for easier matching

    content = text_body.lower() 
    # Check each topic
    if any(keyword in content for keyword in job_offer_keywords):
        return "JobOffer"
    elif any(keyword in content for keyword in job_interest_keywords):
        return "JobInterest"
    elif any(keyword in content for keyword in person_looking_keywords):
        return "PersonLooking"
    elif any(keyword in content for keyword in company_looking_keywords):
        return "CompanyLooking"
    else:
        return None

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

    if not value_exists_in_column("emails", "senderid", sender_id):
        if not is_in_blacklist(sender_id):           
            topic = determine_topic(message_body)
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
                add_to_blacklist(sender_id)
                save_to_database(df_email, "bademails")
        else:
            # logger.info(f"message_body is not good. message_id: {message_id}")
            print(f"sender in the blacklist: message_id: {message_id}")
            new_row['topic'] = "blacklist"
            df_email = df_email._append(new_row, ignore_index=True)
            save_to_database(df_email, "bademails")
    else:
        # if the sender is already in the DB, add only if the message-id was not in the DB
        # we cannot discard the email because the new body  
        # check if it is not a duplication (message-id)
        if not value_exists_in_column("emails", "messageid", message_id):
            try:
                new_row['topic'] = "-same-" # keep the topic unchanged
                df_email = df_email._append(new_row, ignore_index=True)
                save_to_database(df_email, "emails")
            except Exception as e:
                print(f"Error saving email to database: {e}")

    mark_as_processed(message_id)