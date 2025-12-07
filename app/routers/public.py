from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.crud.news_crud import get_published_news, get_published_news_by_id
from app.models.news import News
from app.schemas.news import NewsOut


router = APIRouter(tags = ['public'])


@router.get('/news')
def get_public_news(db: Session = Depends(get_db)):
    return get_published_news(db)


@router.get('/news/{news_id}')
def get_public_news_by_id(news_id: int, db: Session = Depends(get_db)):
    news = get_published_news_by_id(db, news_id)
    if not news:
        raise HTTPException(404, 'News not found!')
    return news


                                # Создать Первого Админа #
# ------------------------------------------------------------------------------------------ #

# from app.schemas.admin import AdminCreate
# from app.models.admin import Admin
# from app.utils.auth import hash_pas

# @router.post('/nado')
# def nado(admin: AdminCreate, db: Session = Depends(get_db)):
#     db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
#     if db_admin:
#         raise HTTPException(status_code=400, detail = 'Email already registered')
#     hashed_pas = hash_pas(admin.password)
#     db_admin = Admin(email = admin.email, hashed_pas = hashed_pas)
#     db.add(db_admin)
#     db.commit()
#     db.refresh(db_admin)
#     return db_admin

# ------------------------------------------------------------------------------------------ #