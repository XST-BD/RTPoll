import hashlib

from fastapi import APIRouter, Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.db.model.user import UserModel, EmailVerification
from app.deps import get_db
from app.service import get_current_user_state
from app.setup import router, limiter, FRONTEND_URL

router = APIRouter()

@router.get('/check')
def check_auth(
    user_id: str = Depends(get_current_user_state)
):

    return {
        "authenticated": user_id is not None,
        "user_id": user_id,
    }

@router.get('/verify_mail')
def verify_mail(
    token: str, db: Session = Depends(get_db)
):
    # token setup
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
        url=f"{FRONTEND_URL}/login",
        status_code=302
    )

@router.get('/resend_mail')
@limiter.limit('5/minute')   # <--- allow max 5 requests per minute per IP
def resend_mail(
    request: Request, token: str, db: Session = Depends(get_db)
):
    verify_mail(token, db)
    return {"detail": "Mail verification sent"}


