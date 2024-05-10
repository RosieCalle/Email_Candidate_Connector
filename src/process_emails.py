# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# # If modifying these SCOPES, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# def main():
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
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     service = build('gmail', 'v1', credentials=creds)

#     # Call the Gmail API to fetch INBOX emails
#     results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
#     messages = results.get('messages', [])

#     if not messages:
#         print('No new messages.')
#     else:
#         message_count = 0
#         for message in messages:
#             msg = service.users().messages().get(userId='me', id=message['id']).execute()
#             # Process the message here
#             # After processing, mark the message as processed
#             mark_as_processed(service, msg['id'])
#             message_count += 1
#         print(f'Processed {message_count} messages.')



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
    job_offer_keywords = ["job offer", "hiring", "vacancy", "open position"]
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
    
    try:
        # Remove timezone name if present
        date_string = date_time.split('(')[0].strip()

        # Parse the date
        date = parsedate_to_datetime(date_string)

        # Format the date
        timestamp = date.strftime('%Y-%m-%d %H:%M:%S')

    except ValueError as e:
        print(f"Error converting date and time: {e}")
        timestamp = None

    df = pd.DataFrame(columns=['subject', 'timestamp', 'messageid', 'threadid', 'body', 'senderid', 'topic'])
    
    sender_id = extract_email(sender_id)

    print("====== process_emails.py ======")
    print(f"\n\nSubject: {subject}")
    print(f"Date/Time: {timestamp}")
    print(f"Sender ID: {sender_id}")
    print(f"Message ID: {message_id}")
    print(f"Thread ID: {thread_id}")
    print(f"Message Body: {message_body[:200]}")


    if value_exists_in_column("emails", "senderid", sender_id):
        if not is_in_blacklist(sender_id):
            topic = determine_topic(message_body)
            if topic is not None:
                df = df.append({'subject': subject, 'timestamp': timestamp, \
                                'messageid': message_id, 'threadid': thread_id, \
                                'body': message_body[:200], 'senderid': sender_id, \
                                'topic': topic}, ignore_index=True)
            else:   
                # logger.info(f"message_body is not good. message_id: {message_id}")
                print(f"message_body is not good. message_id: {message_id}")
                add_to_blacklist(sender_id)
        else:
            mark_as_processed(message_id)

    save_to_database(df, "emails")



# if __name__ == '__main__':
#     main()