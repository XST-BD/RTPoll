from app.db.session import session_local
from passlib.context import CryptContext

def get_db():
    db = session_local

    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)