from fastapi import FastAPI
from app.database.db import engine, Base
from app.routers import auth, admin
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

#Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Routers
app.include_router(auth.router)
app.include_router(admin.router)

@app.get('/')
def root(): return {'message': 'Backend part'}

# @app.post('/register', response_model = AdminOut)
# def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
#     db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
#     if db_admin:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     hashed_pas = hash_pas(admin.password)
#     db_admin = Admin(email = admin.email, hashed_pas = hashed_pas)
#     db.add(db_admin)
#     db.commit()
#     db.refresh(db_admin)
#     return db_admin

# @app.post('/login')
# def login(admin: AdminLogin, db: Session = Depends(get_db)):
#     db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
#     if not db_admin or not verify_pas(admin.password, db_admin.hashed_pas):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data = {'sub': db_admin.email})
#     return {'access_token': access_token, 'token_type': 'bearer'}

# @app.get("/admin/me", response_model=AdminOut)
# def read_admin_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except jwt.JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     admin = db.query(Admin).filter(Admin.email == email).first()
#     if admin is None:
#         raise HTTPException(status_code=403, detail="Not an admin")
#     return admin

if __name__ == '__main__':
    uvicorn.run(app = 'main:app', port = 8000, reload = True)









    # amir