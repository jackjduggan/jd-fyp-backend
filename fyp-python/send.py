import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secret.config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

def send_email(
    sender_email, 
    sender_password, 
    receiver_email, 
    subject, 
    request_details,
    time_requested,
    requester_email,
    unique_id):

    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    body = f"""\
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .email-container {{
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .logo {{
            display: block;
            margin: auto;
            max-width: 200px;
        }}
        .content {{
            margin-top: 20px;
        }}
        .button {{
            display: inline-block;
            margin: 20px 0;
            padding: 10px 20px;
            color: #fff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
        }}
        .button-approve {{
            background-color: #6143E1;
        }}
        .button-deny {{
            background-color: #20115F;
        }}
    </style>
    </head>
    <body>
    <div class="email-container">
        <img src="https://raw.githubusercontent.com/jackjduggan/email-approval-system/main/images/InProv-logo-light-removebg-preview.png" alt="Company Logo" class="logo">
        <h2>Approval Request</h2>
        <p class="content">A new server is requesting approval.<br><br>
            <strong>Request Details</strong>: {request_details}<br>
            <strong>Time Requested</strong>: {time_requested}<br>
            <strong>Requester's Email</strong>: {requester_email}<br>
            <strong>Request Unique ID</strong>: {unique_id}<br>
        Provisioning will not begin until approved.<br> 
        Please reply to this email with <strong>Approve</strong> to approve, or <strong>Deny</strong> to deny.</p>
        <a href="mailto:{sender_email}?subject=Approval Request - Approve&body=Approve" class="button button-approve">Approve</a>
        <a href="mailto:{sender_email}?subject=Approval Request - Deny&body=Deny" class="button button-deny">Deny</a>
    </div>
    </body>
    </html>
    """

    # Create a MIMEText object to represent the email
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Create a MIMEText object for HTML email
    html = MIMEText(body, 'html')

    # Attach the body of the email to the message
    msg.attach(html)

    # Start the SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Close the SMTP session
    server.quit()

# ref: https://medium.com/@thakuravnish2313/sending-emails-with-python-using-the-smtplib-library-e5db3a8ce69a