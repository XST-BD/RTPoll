import os
import smtplib
import ssl 
import secrets
import hashlib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import Request

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db.base import dbengine
from app.db.model.user import EmailVerification

from app.setup import (
    SENDER_MAIL, APP_PASSWORD, SMTP_SERVER, SMTP_PORT_TLS, BACKEND_URL1
)

from app.utils import validate_db_entry



def generate_login_url_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest

    return token, token_hash()


def prepare_verification_link(
    user: str, db: Session
):
    # token setup
    token, token_hash = generate_login_url_token()

    verification = EmailVerification(
        username=user,
        token_hash=token_hash,
    )

    db.add(verification)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Handle unique constraint violations
        validate_db_entry(str(e).lower())

    db.refresh(verification)

    link = f"{BACKEND_URL1}/api/v0/auth/verify_mail?token={token}"
    return link


def send_mail_verification(
    reciever_mail_addr: str, link: str,
):
    # mail setup
    
    receiver_email = reciever_mail_addr
    
    # Email content
    subject = "Account verification email from RTPoll"
    # HTML body with clickable link
    body = f"""
    Thank you for registering an account in RTPoll Website.
    <br>
    <br>
    Please click the following URL to confirm your e-mail address:
    <br>
    <a href="{link}">{link}</a>
    <br>
    <br>
    If you did not register an account in RTPoll Website, please ignore  this mail.
    <br>
    <br>
    <a href="https://github.com/XST-BD">XST-BD Org.</a>
    """

    # --- Create the email message ---
    msg = MIMEMultipart()
    msg['From'] = SENDER_MAIL
    msg['To'] = receiver_email 
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Connect to the server and send the email
        with smtplib.SMTP(str(SMTP_SERVER), int(SMTP_PORT_TLS)) as server:
            server.starttls(context=context) # Secure the connection with TLS
            server.login(str(SENDER_MAIL), str(APP_PASSWORD))
            server.send_message(msg)
            print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"Error: Unable to send email. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_current_user_state(request: Request):
    return request.session.get('user_id')