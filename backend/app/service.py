import os
import smtplib
import ssl 
import secrets
import hashlib

from dotenv import load_dotenv

from email.message import EmailMessage 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.base import dbengine
from app.db.model.user import EmailVerification, UserModel
from app.deps import get_db
from app.setup import app
from app.utils import validate_db_entry

def generate_login_url_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest

    return token, token_hash()


def prepare_verification_link(
    user: str, db: Session
):
    load_dotenv()

    # token setup
    site_url = os.getenv('BACKEND_URL1')
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

    link = f"{site_url}/api/v0/auth/verify_mail?token={token}"
    return link


def send_mail_verification(
    reciever_mail_addr: str, link: str,
):

    load_dotenv()
    # mail setup
    sender_email = os.getenv('MAIL_USERNAME', 'MAIL_USERNAME')
    receiver_email = reciever_mail_addr
    app_password = os.getenv('MAIL_PASSWORD')
    smtp_server = os.getenv('MAIL_SERVER')
    smtp_port_tls = os.getenv('MAIL_PORT_TLS', 587)

    # Email content
    subject = "Account verification email from RTPoll"
    # HTML body with clickable link
    body = f"""
    Thank you for registering an account in RTPoll Website.
    Please click the following URL to confirm your e-mail address:
    <br>
    <a href="{link}">{link}</a>
    <br>
    If you did not register an account in RTPoll website, please ignore  this mail.
    <br>
    <a href="https://github.com/XST-BD">XST-BD Org.</a>
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


@app.get('/api/v0/auth/verify_mail')
def verify_mail(
    token: str, db: Session = Depends(get_db)
):

    load_dotenv()
    # token setup
    site_url = os.getenv('FRONTEND_URL1')

    token_hash = hashlib.sha256(token.encode()).hexdigest()
    record = db.query(EmailVerification).filter(EmailVerification.token_hash==token_hash).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid link")
    
    if record.used: 
        raise HTTPException(status_code=400, detail="Link is already used and expired")
    
    user = (db.query(UserModel).filter(UserModel.username==record.username).first())
    if user is None:
        raise HTTPException(status_code=400, detail="User not found during mail validation")

    user.is_verified = True
    record.used = True

    db.commit()

    return RedirectResponse(
        url=f"{site_url}/login?verified=1",
        status_code=302
    )