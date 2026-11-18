from fastapi import FastAPI,APIRouter,Depends,HTTPException,UploadFile,File
from ..database import SessionLocal
from ..models import Project,FileRef
from .auth import get_current_user
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from typing import Annotated
from datetime import date
from pathlib import Path
import shutil

router = APIRouter( prefix= "/file", tags=["file"])
def get_db():
    db = SessionLocal()
    try:
       yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

BASE_STORAGE = Path("storage")

@router.post("/{proj_id}/uploadFile", status_code = status.HTTP_201_CREATED)
async def upload_file(proj_id:int, db:db_dependency, user: user_dependency, file: UploadFile = File(...)):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    #the flow it recommended first store file in disk and store file path in file table
    project_dir = (BASE_STORAGE /f"user_{user['id']}"/f"project_{proj_id}")
    project_dir.mkdir(parents=True,exist_ok=True)
    file_path= project_dir / file.filename
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    file_record = FileRef(
        proj_id = proj_id,
        filename = file.filename,
        file_path = str(file_path),
        uploaded_at = date.today())
    db.add(file_record)
    db.commit()
    file_id = file_record.id
        
    return {"id": file_id, "proj_id":proj_id}

@router.get("/{proj_id}/all_files", status_code = status.HTTP_200_OK)
async def get_all_proj_files(proj_id:int, db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    proj = ( db.query(Project).filter(Project.user_id==user["id"]).filter(Project.id==proj_id).first())
    if not proj:
        raise HTTPException(status_code=404, detail=" No such project")
    list_files = db.query(FileRef).filter(FileRef.proj_id == proj_id).all()
    return [{"file_id": file.id, "file_name": file.filename, "file_path": file.file_path} for file in list_files]

@router.delete("/{proj_id}/{file_id}/delete",status_code = status.HTTP_204_NO_CONTENT)
async def delete_file(proj_id:int, file_id:int, db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail = "Account not found")
    proj = ( db.query(Project).filter(Project.user_id==user["id"]).filter(Project.id==proj_id).first())
    if not proj:
        raise HTTPException(status_code=404, detail=" No such project")
    file_model = db.query(FileRef).filter(FileRef.proj_id == proj_id).filter(FileRef.id == file_id).first()
    if not file_model:
        raise HTTPException(status_code=404, detail="No such file found")
    file_dir = file_model.file_path
    file_path = Path(file_dir)
    if file_path.exists():
        #for files its diff shutil only works for directories
        file_path.unlink()
    db.delete(file_model)
    db.commit()
    return {"msg" : "file deleted"}

#we need analysis per file
#when delete a file remove it from disk