import os
import uuid

from dotenv import load_dotenv
from pydantic import SecretStr

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=str(os.getenv('MAIL_USERNAME')),
    MAIL_PASSWORD=SecretStr(os.getenv('MAIL_PASSWORD', '')),
    MAIL_FROM=str(os.getenv('MAIL_FROM')),
    MAIL_PORT=int(os.getenv('MAIL_PORT', '587')),
    MAIL_SERVER=str(os.getenv('MAIL_SERVER')), # Example for Gmail, use your provider's SMTP server
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# short and unique poll slug
def generate_poll_slug() -> str:
    return uuid.uuid4().hex[:12]

async def send_poll_email(to, poll_url: str, expires_at):
    
    message = MessageSchema(
        subject="Your poll is live 🎉",
        recipients=[to],
        body=f"""
        Your poll has been created successfully.

        Poll link:
        {poll_url}

        Expires at:
        {expires_at.strftime('%Y-%m-%d %H:%M UTC')}
        """,
        subtype=MessageType("plain"),
    )

    fm = FastMail(conf)
    
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Email failed: {e}")
