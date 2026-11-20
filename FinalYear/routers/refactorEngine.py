from fastapi import APIRouter, HTTPException, Depends
from ..database import SessionLocal
from ..models import Refactorisations,Metrics,Analysis,Project,FileRef
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from typing import Annotated
from .auth import get_current_user
from pathlib import Path
import requests
from datetime import datetime
from .analyze import analyze_source_code,fetch_file
import json
import ast

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

router = APIRouter( prefix = "/refactor",tags=["refactor"])

class AIResponse(BaseModel):
    analysis_id:int
    refactor_id: int
    recommendations: list
    refactored_code: str
    complexity_after: float
    maintainability_after: float
    generated_at: datetime
    
    
class InitialRefactor(BaseModel):
    proj_id : int
    analysis_id:int #past deets
    file_id:int | None = None
    
class RetryRefactor(BaseModel):
    analysis_id:int #past deets
    refactor_id: int| None = None
    user_feedback: str | None = None

def get_file_content(file_path:str):
    content = Path(file_path).read_text()
    return content

#this can be reused by retry and first try since the differentiating logic is located in recs prompt
def create_refactor_prompt(file_content:str, recs: str):
    prompt = f"""
    You are a senior Python software engineer.
    Refactor the code below.
    
    Requirements:
    
    - Preserve functionality exactly.
    - Apply every recommendation provided.
    - Reduce duplication.
    - Improve readability.
    - Improve maintainability.
    - Reduce complexity where possible.
    - Return the COMPLETE source file.
    """
    
    prompt += f"""
    Recommendations:
    {recs}
    
    Code:
    {file_content}
    
    Return only Python code.
    No explanations.
    No markdown.
    """
    return prompt

def create_recommendations_prompt(file_content:str, cognitive_score: int,cyclomatic_score:int,
                  halstead_volume: float,loc: int,mi: float,cbo: float,
                  lcom:float,final_complex_score: float,final_maintain_score:float):
    prompt = """You are a senior Python software engineer.
                Analyze the code and generate refactoring recommendations.
                
                """
    prompt += f"""
                Requirements:
                
                1. Recommendations must be concrete and implementable.
                2. Recommendations must be specific to the supplied code.
                3. Recommendations must describe code changes.
                4. Recommendations should target:
                       - high cognitive complexity
                       - duplicated logic
                       - excessive nesting
                       - poor naming
                       - long methods
                       - maintainability issues

                Do NOT generate vague recommendations such as:
                - improve maintainability
                - improve readability
                - separate concerns
                - simplify the code
                
                Instead generate recommendations such as:
                - Extract helper method X from method Y
                - Rename variable A to B
                - Move repeated logic into a shared function
                - Replace nested conditional with guard clauses
   
                Below are Static Analysis Results to help you structure recommendations:
                1) cognitive complexity score: {cognitive_score}
                2) cyclomatic complexity score: {cyclomatic_score}
                3) halstead volume: {halstead_volume}
                4) lines of code: {loc}
                5) maintainability index: {mi}
                6) coupling between objects: {cbo}
                7) lack of cohesion in methods: {lcom}
                
                Final Scores calculated:
                complexity: {final_complex_score}
                maintainability: {final_maintain_score}
                
                """
    prompt += "code: " + file_content
    prompt += """

                Return JSON and return only **5 Recommendations**:
                
                {
                "recommendations": [
                    "recommendation 1",
                    "recommendation 2",
                    "recommendation 3"]
                    }
            """
    return prompt

def prompt_retry_rec(code: str ,complexity_score: float , maintainability_score: float, user_feedback: str):
    prompt = f"""
            You are a senior Python software engineer whose expertise lie in implementing constructive feedback thoroughly
            ,reducing complexity of code as much as possible as well as increasing maintainability of code. You are to provide recommendations
            on provided code based on requirements given below:
            
            """
    prompt += f"""
                Requirements:
                
                1. Recommendations must be concrete and implementable.
                2. Recommendations must be specific to the supplied code.
                3. Recommendations must describe code changes.
                4. Recommendations should target:
                       - high cognitive complexity
                       - duplicated logic
                       - excessive nesting
                       - poor naming
                       - long methods
                       - maintainability issues

                Do NOT generate vague recommendations such as:
                - improve maintainability
                - improve readability
                - separate concerns
                - simplify the code
                
                Instead generate recommendations such as:
                - Extract helper method X from method Y
                - Rename variable A to B
                - Move repeated logic into a shared function
                - Replace nested conditional with guard clauses
                
                """
    prompt += f"""
                You have also been given the constructive feedback of a user which has to be implemented in the code you send back.
                DO NOT TRY TO IGNORE THIS FEEDBACK. Use it to structure your recommendations inorder to suit the feedback and code better.
                
                {user_feedback}
                
                Here are the current complexity and maintainability scores of the given code:
                1. complexity : {complexity_score}
                2. maintainability : {maintainability_score}
                
                """
    prompt += "code: " + code
    prompt += """

                Return JSON and return only **5 Recommendations**:
                
                {
                "recommendations": [
                    "recommendation 1",
                    "recommendation 2",
                    "recommendation 3"]
                    }
            """
    return prompt
    
    

async def store_ref_results(analysis_id:int, recs: str, result2: str, generated: datetime, db:db_dependency):
    ref_model = Refactorisations(
        analysis_id = analysis_id,
        recommendations = recs,
        refactored_code = result2,
        generated_at = generated
        )
    db.add(ref_model)
    db.commit()
    db.refresh(ref_model)
    res = {"id": ref_model.id, "recommendations": recs, "refactored_code": result2
           , "generated_at": generated}
    return res

async def update_ref_results(ref_id: int, recs: str, refcode: str, generated: datetime, db: db_dependency):
    ref_model = db.query(Refactorisations).filter(Refactorisations.id == ref_id).first()
    ref_model.recommendations = recs
    ref_model.refactored_code = refcode
    ref_model.generated_at = generated
    db.add(ref_model)
    db.commit()
    return {"id": ref_model.id, "refactored_code": refcode,"generated_at": generated}
        
        
#first refactoring and recommendations
@router.post("/first_refactor",status_code=status.HTTP_201_CREATED)
async def get_first_refactor(refactor_deets: InitialRefactor,db:db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code = 401, detail="User not authenticated")
    analysis_id = refactor_deets.analysis_id
    file_id = refactor_deets.file_id
    proj_id = refactor_deets.proj_id
    proj_model = db.query(Project).filter(Project.user_id == user["id"]).filter(Project.id == proj_id).first()
    if not proj_model:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    analysis_obj = db.query(Analysis).filter(Analysis.id==analysis_id).first()
    if not analysis_obj:
        raise HTTPException(status_code=404, detail="No such analysis found")
    file_model = db.query(FileRef).filter(FileRef.proj_id == proj_id).filter(FileRef.id == file_id).first()
    if not file_model:
        raise HTTPException(status_code=404, detail="No such file found to analyze")
    
    file_path = file_model.file_path
    user_code = get_file_content(file_path)
    
    metrics_res = db.query(Metrics).filter(Metrics.analysis_id == analysis_id).first()
    analysis_obj.retries += 1
    db.add(analysis_obj)
    db.commit()                #updating retries column
    
    #gonna need to change or smth cz userfeedbakc is not in the initial refactor
    prompt_rec = create_recommendations_prompt(user_code,metrics_res.cognitive_score,metrics_res.cyclomatic_score,metrics_res.halstead_volume,
                           metrics_res.loc,metrics_res.maintainability_index,metrics_res.cbo,metrics_res.lcom,
                           analysis_obj.complexity_score,analysis_obj.maintainability_score)

    response1 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_rec,
            "stream":False,
            "format":"json",
            }
        )
    
    data1 = response1.json()
    if "error" in data1:
        response1 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_rec,
            "stream":False,
            "format":"json",
            }
        )
        data1 = response1.json()
        
    result1 = json.loads(data1["response"])
    
    recs = str(result1["recommendations"])
    
    prompt_ref = create_refactor_prompt(user_code,recs)
    response2 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_ref,
            "stream":False,
            }
        )
    

    data2 = response2.json()
    
    if "error" in data2:
        response2 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_ref,
            "stream":False,
            "format":"json",
            }
        )
        data2 = response2.json()
    
    result2 = data2["response"]

    generated = datetime.now().date()
    
    res = await store_ref_results(analysis_id, recs, result2, generated, db)
    return res  #for the UI analysis,id,rec,ref,generatedat


@router.post("/RetryRefactor",status_code=status.HTTP_201_CREATED)
async def get_retry_refactor(refactor_deets: RetryRefactor,db:db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code = 401, detail="User not authenticated")
    analysis_id = refactor_deets.analysis_id
    user_feedback = refactor_deets.user_feedback
    analysis_obj = db.query(Analysis).filter(Analysis.id==analysis_id).first()
    if not analysis_obj:
        raise HTTPException(status_code=404, detail="No such analysis found")
    
    
    ref_id = refactor_deets.refactor_id
    ref = db.query(Refactorisations).filter(Refactorisations.analysis_id== analysis_id).filter(Refactorisations.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="No such refactorisations made")
    code = ref.refactored_code
    
    analysis_obj.retries += 1
    db.add(analysis_obj)
    db.commit()                #updating retries column
    
    #complexity and maintainability after first refactor + user feedback r what matter in retry
    complexity_score = ref.complexity_after
    maintainability_score = ref.maintainability_after
    
    prompt_rec = prompt_retry_rec(code,complexity_score, maintainability_score, user_feedback)
    

    response1 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_rec,
            "stream":False,
            "format":"json",
            }
        )
    
    data1 = response1.json()
    if "error" in data1:
        response1 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_rec,
            "stream":False,
            "format":"json",
            }
        )
        data1 = response1.json()
        
    result1 = json.loads(data1["response"])
    print(result1)
    
    recs = str(result1["recommendations"])
    
    prompt_ref = create_refactor_prompt(code,recs)
    response2 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_ref,
            "stream":False,
            }
        )
    

    data2 = response2.json()
    
    if "error" in data2:
        response2 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_ref,
            "stream":False,
            "format":"json",
            }
        )
        data2 = response2.json()
    
    result2 = data2["response"]
    print(result2)
    generated = datetime.now().date()
    res = await update_ref_results(ref_id, recs, result2, generated, db) #update exisitng entry instead of new records.
    return res  #for the UI analysis,id,rec,ref,generatedat


@router.post("/{proj_id}/{analysis_id}/{refactor_id}/analyze",status_code=status.HTTP_201_CREATED)
async def analyze_refactored(proj_id:int,analysis_id:int,refactor_id:int, db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code = 401, detail="User not authenticated")
    proj_model = db.query(Project).filter(Project.user_id == user["id"]).filter(Project.id == proj_id).first()
    if not proj_model:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    analysis_obj = db.query(Analysis).filter(Analysis.proj_id== proj_id).filter(Analysis.id == analysis_id).first()
    if not analysis_obj:
        raise HTTPException(status_code=404, detail=" No such analysis made")
    data = db.query(Refactorisations).filter(Refactorisations.analysis_id== analysis_id).filter(Refactorisations.id== refactor_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="No such refactorisation made")
    refactored_code = data.refactored_code

    refactored_code = refactored_code.replace("```python", "")
    refactored_code = refactored_code.replace("```", "")
    refactored_code = refactored_code.strip()
    ast_tree = ast.parse(refactored_code)
    score_model = await analyze_source_code(ast_tree,proj_id,db,None,analysis_id)
    data.complexity_after = score_model["complexity_score"]
    data.maintainability_after = score_model["maintainability_score"]
    db.add(data)
    db.commit()
    return {"proj_id":proj_id, "analysis_id":analysis_id, "ref_id": refactor_id, "complexity_after":score_model["complexity_score"],
            "maintainability_after": score_model["maintainability_score"]}


#add a get refactored code? or smth    