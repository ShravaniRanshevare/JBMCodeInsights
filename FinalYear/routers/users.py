from fastapi import FastAPI,APIRouter,Depends,HTTPException
from ..database import SessionLocal
from ..models import Users,Analysis,Project
from .auth import get_current_user,bcrypt_context
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from typing import Annotated
from pathlib import Path
import shutil

class User_req(BaseModel):
    username: str
    
class User_req2(BaseModel):
    user_email: str
    
class user_pass_req(BaseModel):
    old_pass:str
    new_pass:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
BASE_STORAGE = Path("storage")

router = APIRouter(prefix = "/user", tags= ["user"])

@router.get("/profile",status_code=status.HTTP_200_OK)
async def get_profile(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code = 401, detail="not authenticated, retry")
    user_details = db.query(Users).filter(Users.id==user["id"]).first()
    if not user_details:
        raise HTTPException(status_code = 404, detail="account not found")
    return {"username": user_details.username, "email": user_details.user_email}

@router.put("/username",status_code= status.HTTP_204_NO_CONTENT)
async def update_username(user_req: User_req, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail = "not authenticated , cannot update")
    user_model = db.query(Users).filter(Users.id==user["id"]).first()
    if not user_model:
        raise HTTPException(status_code = 404, detail="account not found")
    user_model.username = user_req.username
    db.add(user_model)
    db.commit()
    
@router.put("/useremail",status_code= status.HTTP_204_NO_CONTENT)
async def update_email(user_req: User_req2, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail = "not authenticated , cannot update")
    user_model = db.query(Users).filter(Users.id==user["id"]).first()
    if not user_model:
        raise HTTPException(status_code = 404, detail="account not found")
    user_model.user_email = user_req.user_email
    db.add(user_model)
    db.commit()
    
@router.delete("/delete_acc",status_code= status.HTTP_204_NO_CONTENT)
async def delete_acc(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail = "not authenticated , cannot delete account")
    
    user_model = db.query(Users).filter(Users.id==user["id"]).first()
    if not user_model:
        raise HTTPException(status_code = 404, detail="account not found")
    storage_path = Path(f"{BASE_STORAGE}/user_{user['id']}")
    if storage_path.exists():
        shutil.rmtree(storage_path,ignore_errors=True) #so that we dlete on disk storage of user's files
    db.delete(user_model)
    db.commit()
    
@router.put("/user_password",status_code= status.HTTP_204_NO_CONTENT)
async def update_password(user_req: user_pass_req, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail = "not authenticated , cannot update")
    old_pass=user_req.old_pass
    new_pass = user_req.new_pass
    user_model = db.query(Users).filter(Users.id==user["id"]).first()
    if not user_model:
        raise HTTPException(status_code = 404, detail="account not found")
    curr_pass = user_model.hashed_password
    if not bcrypt_context.verify(old_pass,curr_pass):
        raise HTTPException(status_code=401, detail="wrong old password")
    user_model.hashed_password = bcrypt_context.hash(new_pass)
    db.add(user_model)
    db.commit()
    



    


    