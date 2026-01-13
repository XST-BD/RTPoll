import os
import smtplib
import ssl 
import secrets

from email.message import EmailMessage 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

def generate_temporary_slug():
    return secrets.token_urlsafe(32)

def send_mail_verification(reciever_mail_addr: str):

    load_dotenv()

    sender_email = os.getenv('MAIL_USERNAME', 'MAIL_USERNAME')
    app_password = os.getenv('MAIL_PASSWORD')
    smtp_server = os.getenv('MAIL_SERVER')
    smtp_port_tls = os.getenv('MAIL_PORT_TLS', 587)
    site_url = os.getenv('FRONTEND_URL1')

    token_slug = generate_temporary_slug()
    link = f"{site_url}/login?token={token_slug}"


    receiver_email = reciever_mail_addr

    # Email content
    subject = "An Email from RTPoll"
    # HTML body with clickable link
    body = f"""
    Hi there,

    Click the link below to complete your registration:

    <a href="{link}">{link}</a>

    This link is one-time use.

    Thanks!
    """

    # --- Create the email message ---
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email 
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # --- Send the email ---
    smtp_server = smtp_server
    smtp_port_tls = smtp_port_tls 

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Connect to the server and send the email
        with smtplib.SMTP(str(smtp_server), int(smtp_port_tls)) as server:
            server.starttls(context=context) # Secure the connection with TLS
            server.login(str(sender_email), str(app_password))
            server.send_message(msg)
            print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"Error: Unable to send email. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
