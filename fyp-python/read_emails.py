import imaplib
import email
from email.policy import default
import os
from secret.config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

# Connect to the IMAP server and log in
m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
m.login(SENDER_EMAIL, SENDER_PASSWORD)
m.select('inbox')  # Select the inbox

# Search for all emails
result, data = m.uid('search', None, 'ALL')
print(f"Search result: {result}, Data: {data}")

if result == 'OK':
    for num in data[0].split():
        uid = num.decode('utf-8')

        # Fetch the email by UID
        result, data = m.uid('fetch', uid, '(RFC822.HEADER)')
        print(f"Fetch result: {result}")
        if result == "OK" and data[0] is not None:
            # Parse the email header
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email, policy=default)

            # Extract the subject
            subject = email_message.get('Subject', 'No Subject')
            print(f"UID: {uid}, Subject: {subject}")
        else:
            print(f"Failed to fetch or no data for UID {uid}")

# Logout from the server
m.close()
m.logout()
