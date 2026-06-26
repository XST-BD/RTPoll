import resend
import secrets
import hashlib

from sqlalchemy.orm import Session

from app.db.model.user import EmailVerification


from app.setup.vars import (
    SENDER_MAIL, RESEND_API_KEY,  FRONTEND_URL
)

VERIFICATION_TOKEN_LIFETIME = 300

# ====================== MAIL SERVICE CODES ====================== #

def generate_login_url_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return token, token_hash


def prepare_verification_link(db: Session, email: str, token_type: str, extra: str | None = None):
    # token setup
    token, token_hash = generate_login_url_token()

    verification = db.query(EmailVerification).filter(
        EmailVerification.token_type==token_type, EmailVerification.email==email
    ).first()

    if verification:
        verification.token_type = token_type
        verification.token_hash = token_hash
        verification.used = False
        # verification.expires_at = datetime.now(timezone.utc) + timedelta(VERIFICATION_TOKEN_LIFETIME)
    else:
        verification = EmailVerification(
            email=email, 
            token_type=token_type, 
            token_hash=token_hash,
            # expires_at = datetime.now() + timedelta(VERIFICATION_TOKEN_LIFETIME)
        )
        db.add(verification)

    if verification.token_type == "forgot_pass":
        link = f"{FRONTEND_URL}/recover-pass?t={token}"
    elif verification.token_type == "email_change" and extra:
        verification.extra_data = extra
        link = f"{FRONTEND_URL}/verify-mail?t={token}"
    else:
        link = f"{FRONTEND_URL}/verify-mail?t={token}"

    db.commit()

    return link


def send_mail_verification(
    purpose: str, reciever_mail_addr: str, link: str,
):
    # mail setup
    receiver_email = reciever_mail_addr
    
    # Email content
    subject_new_acc = "Account verification email from RTPoll"
    subject_rec_acc = "Password recovery email from RTPoll"
    subject_exc_acc = "Account exchange email from RTPoll"

    # HTML body with clickable link
    body_new_acc = f"""
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

    body_rec_acc = f"""
    Here's your password recovery link. Please click the following URL to restore your password:
    <br>
    <a href="{link}">{link}</a>
    <br>
    <br>
    If you did not request for password recovery, you can ignore this mail.
    <br>
    <br>
    <a href="https://github.com/XST-BD">XST-BD Org.</a>
    """

    body_exc_acc = f"""
    Here's your accout exchange link. Please click the following URL to exchange your RTPoll account:
    <br>
    <a href="{link}">{link}</a>
    <br>
    <br>
    If you did not request for password recovery, you can ignore this mail.
    <br>
    <br>
    <a href="https://github.com/XST-BD">XST-BD Org.</a>
    """

    subject = ''
    body = ''
    
    if purpose == "NEW":
        subject = subject_new_acc
        body = body_new_acc
    elif purpose == "REC":
        subject = subject_rec_acc
        body = body_rec_acc
    elif purpose == "CHN":
        subject = subject_exc_acc
        body = body_exc_acc

    # msg = MIMEMultipart()
    # msg['From'] = SENDER_MAIL
    # msg['To'] = receiver_email 
    # msg['Subject'] = subject
    # msg.attach(MIMEText(body, 'html'))

    # # Create a secure SSL context
    # context = ssl.create_default_context()

    # try:
    #     # Connect to the server and send the email
    #     with smtplib.SMTP(str(SMTP_SERVER), int(SMTP_PORT_TLS)) as server:
    #         server.starttls(context=context) # Secure the connection with TLS
    #         server.login(str(SENDER_MAIL), str(APP_PASSWORD))
    #         server.send_message(msg)
    #         print("Email sent successfully!")

    # except smtplib.SMTPException as e:
    #     print(f"Error: Unable to send email. {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")

 
    # --- Send the email message ---
    resend.api_key = RESEND_API_KEY

    r = resend.Emails.send({
      "from": SENDER_MAIL,
      "to": receiver_email,
      "subject": subject,
      "html": body,
    })