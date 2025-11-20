from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminOut
from app.dependencies import get_current_admin
from app.utils.auth import hash_pas
from app.utils.crud import delete_user, delete_user_by_email, get_all_admins
import logging


router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)


@router.get("/me", response_model = AdminOut)
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


@router.delete('/users/id/{admin_id}')
def delete_admin(admin_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    logger.info(f"Deleting admin {admin_id} by {current_admin.email}")
    success = delete_user(db, admin_id)
    if not success:
        raise HTTPException(status_code = 404, detail = 'Admin not found!')
    return {'message': 'Admin deleted succesfully'}


@router.delete('/users/email/{admin_email}')
def delete_admin_by_email(admin_email: str, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    logger.info(f"Deleting admin {admin_email} by {current_admin.email}")
    success = delete_user_by_email(db, admin_email)
    if not success:
        raise HTTPException(status_code = 404, detail = 'Admin not found!')
    return {'message': 'Admin deleted succesfully'}


@router.get('/users')
def get_admins(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    logger.info(f"Getting all admins by {current_admin.email}")

    admins = get_all_admins(db)
    return admins