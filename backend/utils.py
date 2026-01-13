import re
import dns.resolver
import dns.exception
from fastapi.exceptions import HTTPException

def validate_email(email_addr: str):
    # Step 1: Basic format check
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email_addr):
        return False

    # Step 2: Check if domain has MX record
    domain = email_addr.split("@")[1]
    try:
        answers = dns.resolver.resolve(domain, "MX")
        return len(answers) > 0
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return False


def validate_user_input(username: str, email: str, password: str):
    # Username: only letters, numbers, underscores
    if not re.fullmatch(r'\w+', username):
        return "Username can only contain letters, numbers, and underscores"
    
    if len(username) < 4:
        return "Username can't have less than 4 characters"

    # Email: simple regex check
    if not validate_email(email):
        return "Invalid email format"

    # Password: min len 8
    if len(password) < 8:
        return "Password must be at least 8 characters long"

    return None


def validate_db_entry(err_msg: str):

    if "username" in err_msg:
            raise HTTPException(status_code=400, detail="Username already taken")
    elif "email" in err_msg:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        raise HTTPException(status_code=400, detail="Database error")
