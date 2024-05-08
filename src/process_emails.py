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
import pandas as pd



def mark_as_processed(service, message_id):
    # Here you would apply a label to mark the message as processed
    # This is a placeholder function
    pass

def process_email_data(subject: str, date_time: str, sender_id: str, message_id: str, thread_id: str, message_body: str ):
    """ Analitycs of the email data
        body parsing: look for phone number, linkedin account
        email_rejection: there is not attachemnt and body is not related to a job
        thread_analysis: .... 

    """
    
    # Convert the string to a datetime object
    date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    # Convert the datetime object to a timestamp
    timestamp = date_time_obj.timestamp()

    df = pd.DataFrame(columns=['subject', 'timestamp', 'messageid', 'threadid', 'body', 'senderid'])

    print(f"\n\nSubject: {subject}")
    print(f"Date/Time: {timestamp}")
    print(f"Sender ID: {sender_id}")
    print(f"Message ID: {message_id}")
    print(f"Thread ID: {thread_id}")
    print(f"Message Body: {message_body}")


    if exist_in_database(sender_id, "emails"): 
        if is_in_black_list(sender_id):
            # how to use subject to determine if the email go or not to the DB ?
            if isgood(subject):
                # how to use the body to determine if the email go or not to the DB ?
                if isgood(message_body):
                    df = df.append({'subject': subject, 'timestamp': timestamp, \
                                    'messageid': messageid, 'threadid': threadid, \
                                    'body': body, 'senderid': senderid}, ignore_index=True)
                else:   
                    logger.info(f"message_body is not good. message_id: {message_id}")
            else:   
                logger.info(f"subject is not good. message_id: {message_id}")







if __name__ == '__main__':
    main()