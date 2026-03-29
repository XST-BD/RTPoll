import re
import dns.resolver
import dns.exception

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
