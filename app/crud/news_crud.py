from sqlalchemy.orm import Session
from app.models.news import News
from app.schemas.news import NewsCreate


# Получить все новости
def get_news(db: Session):
    news = db.query(News).all()

    return news


# Создать новость
def create_news(db: Session, title: str, content: str, image_path: str = None):
    db_news = News(title = title, content = content, image_url = image_path)

    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    return db_news