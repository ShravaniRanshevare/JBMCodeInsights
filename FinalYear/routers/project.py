from fastapi import FastAPI,APIRouter,Depends,HTTPException,UploadFile,File
from ..database import SessionLocal
from ..models import Users,Project,FileRef,Analysis
from .auth import get_current_user
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from typing import Annotated
from datetime import date
from pathlib import Path
import shutil

router = APIRouter( prefix ='/project', tags = ['project'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
BASE_STORAGE = Path("storage")


@router.get("/all", status_code= status.HTTP_200_OK)
async def get_all_user_projects(db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    list_projs = db.query(Project).filter(Project.user_id == user["id"]).all()
    return [ {"id": proj.id, "name": proj.name, "created_at": proj.created_at} for proj in list_projs]

@router.get("/{proj_id}",status_code=status.HTTP_200_OK)
async def get_project(proj_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    proj = db.query(Project).filter(Project.user_id == user["id"]).filter(Project.id==proj_id).first()
    if not proj:
        raise HTTPException(status_code=404,detail="Project not found")
    return proj

@router.post("/create/{proj_name}",status_code=status.HTTP_201_CREATED)
async def create_project(proj_name:str,db:db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    proj_model = Project(
        user_id = user["id"],
        name = proj_name,
        created_at = date.today())
    db.add(proj_model)
    db.commit()
    return {"id": proj_model.id}
    
    

@router.put("/update",status_code= status.HTTP_204_NO_CONTENT)
async def update_proj_name(proj_id:int, proj_name: str,db:db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    proj_model = db.query(Project).filter(Project.user_id == user["id"]).filter(Project.id == proj_id).first()
    if not proj_model:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    proj_model.name = proj_name
    db.add(proj_model)
    db.commit()

@router.delete("/{proj_id}/delete-proj",status_code= status.HTTP_204_NO_CONTENT)
async def delete_proj(proj_id:int ,db:db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    proj_model = db.query(Project).filter(Project.user_id == user["id"]).filter(Project.id == proj_id).first()
    if not proj_model:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    proj_dir = (f"{BASE_STORAGE}/user_{user['id']}/project_{proj_id}")
    proj_path = Path(proj_dir)
    if proj_path.exists():
        shutil.rmtree(proj_path,ignore_errors=True)
    db.delete(proj_model)
    db.commit()
    
@router.get("/{proj_id}/all-analysis",status_code = status.HTTP_200_OK)
async def get_all_analysis(proj_id:int,db:db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Account not found")
    list_of_analysis  = db.query(Analysis).filter(Project.user_id == user["id"]).filter(Analysis.proj_id == proj_id).all()
    return [ {"analysis_id": analysis.id , "analysis_complexity_score": analysis.complexity_score , "analysis_maintainability_score": analysis.maintainability_score}
             for analysis in list_of_analysis ]





    
    