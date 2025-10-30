from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import SessionLocal, Base, engine, get_db
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminLogin, AdminOut
from app.utils.auth import hash_pas, verify_pas, create_access_token
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.utils.auth import SECRET_KEY, ALGORITHM
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Application
app = FastAPI(title = 'INAI API')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)


# Tables
Base.metadata.create_all(bind = engine)


@app.get('/')
def root(): return {'message': 'Backend part'}

@app.post('/register', response_model = AdminOut)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pas = hash_pas(admin.password)
    db_admin = Admin(email = admin.email, hashed_pas = hashed_pas)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@app.post('/login')
def login(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin or not verify_pas(admin.password, db_admin.hashed_pas):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data = {'sub': db_admin.email})
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get("/admin/me", response_model=AdminOut)
def read_admin_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin is None:
        raise HTTPException(status_code=403, detail="Not an admin")
    return admin

if __name__ == '__main__':
    uvicorn.run(app = 'main:app', port = 8000, reload = True)