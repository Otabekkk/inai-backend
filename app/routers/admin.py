from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminOut
from app.dependencies import get_current_admin
from app.utils.auth import hash_pas
import logging

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)

@router.get("/me", response_model=AdminOut)
def read_admin_me(admin: Admin = Depends(get_current_admin)):
    return admin

@router.post('/users', response_model = AdminOut)
def create_admin(admin: AdminCreate, current_admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    logger.info(f"Creating new admin by {current_admin.email}")
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pas = hash_pas(admin.password)
    db_admin = Admin(email = admin.email, hashed_pas = hashed_pas)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin