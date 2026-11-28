from fastapi import FastAPI,APIRouter,Depends,HTTPException
from ..database import SessionLocal
from ..models import Users
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel,Field
from jose import jwt,JWTError
from typing import Annotated,Optional
from passlib.context import CryptContext
from datetime import timedelta,datetime,timezone
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

router = APIRouter( prefix ="/auth", tags=["auth"])

SECRET_KEY = "SHRIYASHRAVINFINITYANDBEYOND"
ALGORITHM = 'HS256'
bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated='auto')


oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "/auth/login")

class User_Req(BaseModel):
    username:str = Field(min_length=3)
    user_email: str = Field(min_length=3)
    password: str = Field(min_length=3,max_length=30)
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]

def authenticate_user(userdeets,db:db_dependency):
    user_model = db.query(Users).filter(Users.username == userdeets.username).first()
    if not user_model:
        return False
    hash_pass = user_model.hashed_password
    if not bcrypt_context.verify(userdeets.password,hash_pass):
        return False
    return user_model

def create_token(user_id: int, username: str,  expires_delta: timedelta):
    payload = {"id":user_id,"username":username}
    expire = datetime.now(timezone.utc)+ expires_delta
    payload.update({"exp":expire})
    token = jwt.encode(payload,SECRET_KEY,algorithm = ALGORITHM)
    return token

def get_current_user(token:Annotated[dict,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username :str = payload.get('username')
        userid:int=payload.get('id')
        if username is None or userid is None :
            raise HTTPException(status_code =401 , detail='could not validate credentials')
        return {"id":userid, "username":username}
    except JWTError:
        raise HTTPException(status_code=401,detail="login could not be processed")

@router.post("/create_account",status_code=status.HTTP_201_CREATED)
async def sign_in(user_req:User_Req,db:db_dependency):
    print(user_req)
    hashed_password = bcrypt_context.hash(user_req.password)
    user_model = Users(
        username = user_req.username,
        user_email = user_req.user_email,
        hashed_password = hashed_password)
    db.add(user_model)
    db.commit()
    
@router.post("/login",status_code = status.HTTP_201_CREATED)
async def login(user_model: Annotated[OAuth2PasswordRequestForm,Depends()] ,db:db_dependency):
    user = authenticate_user(user_model,db) #username
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    token = create_token(user.id,user.username,timedelta(minutes=30))
    return {'access_token':token,'token_type':'bearer'}
    
    
