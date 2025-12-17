from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.admin import Admin
from app.models.news import News
from app.schemas.admin import AdminCreate, AdminOut
from app.schemas.news import NewsCreate, NewsOut
from app.dependencies import get_current_admin
from app.utils.auth import hash_pas
from app.utils.save_news import save_upload_file
from app.crud.admin_crud import delete_user, delete_user_by_email, get_all_admins
from app.crud.news_crud import create_news, get_all_news,  delete_news_by_id, get_news_by_id
from fastapi import UploadFile, File
from pathlib import Path
import logging


router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)


@router.get("/me", response_model = AdminOut)
def read_admin_me(admin: Admin = Depends(get_current_admin)):
    return admin


# ------------------------- РАБОТА С УЧЕТКАМИ АДМИНОВ ------------------------- #
@router.post('/users', response_model = AdminOut)
def create_admin(admin: AdminCreate, current_admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    logger.info(f"Creating new admin by {current_admin.email}")
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail = 'Email already registered')
    
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
    logger.info(f'Getting all admins by {current_admin.email}')

    admins = get_all_admins(db)
    return admins
# ----------------------------------------------------------------------------- #


# ---------------------------------- НОВОСТИ ---------------------------------- #
@router.post('/news', response_model = NewsOut)
def news_create( 
    db: Session = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin),
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(...),
    file: UploadFile = File(None)
    ):
    logger.info(f'Creating news by {current_admin.email}')
    
    image_path = None
    
    if file:
        image_path = save_upload_file(file, Path('app/media/news'))

    db_news = create_news(db, title, content, image_path, published)

    return db_news


@router.get('/news')
def get_news(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    logger.info(f'Getting all news by {current_admin.email}')

    db_news = get_all_news(db)

    return db_news


@router.delete('/news/{news_id}')
def delete_news(news_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    logger.info(f"Deleting news {news_id} by {current_admin.email}")
    success = delete_news_by_id(db, news_id)
    if not success:
        raise HTTPException(status_code=404, detail='News not found!')
    return {'message': 'News deleted successfully'}

# TODO
# Написать put роут для новостей

@router.put('/news/{news_id}', response_model = NewsOut)
def update_news(
    news_id: int, 
    db: Session = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin),
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(...),
    file: UploadFile = File(None)):

    logger.info(f"Editing news {news_id} by {current_admin.email}")

    db_news = get_news_by_id(db, news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail='Новость не найдена')
    
    image_path = db_news.image_url
    if file:
        image_path = save_upload_file(file, Path('app/media/news'))

    db_news.title = title
    db_news.content = content
    db_news.image_url = image_path


    db.commit()
    db.refresh(db_news)
    return db_news