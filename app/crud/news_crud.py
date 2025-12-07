from sqlalchemy.orm import Session
from app.models.news import News
from app.schemas.news import NewsCreate


# Получить все новости
def get_all_news(db: Session):
    news = db.query(News).all()

    return news


# Получить опубликованные новости
def get_published_news(db: Session):
    news = db.query(News).filter(News.published == True).all()

    return news

def get_published_news_by_id(db: Session, news_id):
    news = db.query(News).filter(News.published == True, News.id == news_id).first()
    
    return news


# Создать новость
def create_news(db: Session, title: str, content: str, image_path: str = None, published: bool = False):
    db_news = News(title = title, content = content, published = published, image_url = image_path)

    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    return db_news


# Удалить новость (id)
def delete_news_by_id(db: Session, news_id: int):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        return False
    db.delete(news)
    db.commit()
    return True