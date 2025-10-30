from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminLogin
from app.utils.auth import verify_pas, create_access_token
import logging

router = APIRouter(prefix = '/auth', tags = ['auth'])
logger = logging.getLogger(__name__)

@router.post('/login')
def login(admin: AdminLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {admin.email}")
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin or not verify_pas(admin.password, db_admin.hashed_pas):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data = {'sub': db_admin.email})
    return {'access_token': access_token, 'token_type': 'bearer'}