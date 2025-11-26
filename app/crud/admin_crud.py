from sqlalchemy.orm import Session
from app.models.admin import Admin

# Удалить админа (id)
def delete_user(db: Session, admin_id: int):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        return False
    db.delete(admin)
    db.commit()
    return True

# Удалить админа (email)
def delete_user_by_email(db: Session, admin_email: str):
    admin = db.query(Admin).filter(Admin.email == admin_email).first()
    if not admin:
        return False
    db.delete(admin)
    db.commit()
    return True

# Достать всех админов
def get_all_admins(db: Session):
    admins = db.query(Admin).all()
    
    return admins