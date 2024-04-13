def main():
    # Initialize the Gmail API service
    service = gmail_authenticate()

    # Load the list of already downloaded message IDs
    downloaded_message_ids = load_downloaded_message_ids()

    # Search for unread messages
    messages = search_messages(service, "is:unread")

    # Filter out messages that have already been downloaded
    new_messages = [msg for msg in messages if msg['id'] not in downloaded_message_ids]

    # Process and download new messages
    for msg in new_messages:
        # Process the message (e.g., extract content and attachments)
        email_content, attachments = process_message(service, msg)

        # Save the email and attachments
        save_emails_and_attachments([email_content], attachments)

        # Add the message ID to the list of downloaded message IDs
        downloaded_message_ids.append(msg['id'])
        save_downloaded_message_ids(downloaded_message_ids)