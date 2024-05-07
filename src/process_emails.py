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

    print(f"\n\nSubject: {subject}")
    print(f"Date/Time: {date_time}")
    print(f"Sender ID: {sender_id}")
    print(f"Message ID: {message_id}")
    print(f"Thread ID: {thread_id}")
    print(f"Message Body: {message_body}")

    if sender_id "not existe on the database"
        if sender_id "is not in the black_list"
            # how to use subject to determine if the email go or not to the DB ?
            # how to use the body to determine if the email go or not to the DB ?
            






if __name__ == '__main__':
    main()