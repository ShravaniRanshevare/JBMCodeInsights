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
import re

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
    return f"""
You are a senior Python software engineer.

TASK:
Refactor the supplied Python code.

RECOMMENDATIONS TO IMPLEMENT:
{recs}

SOURCE CODE:
{file_content}

MANDATORY RULES:

1. Implement ALL recommendations.
2. Preserve functionality exactly.
3. Do not remove classes.
4. Do not remove public methods.
5. If helper methods are introduced, keep the original public methods.
6. Reduce duplication.
7. Reduce nesting.
8. Improve readability.
9. Improve maintainability.
10. Reduce complexity where possible.

FUNCTIONALITY PRESERVATION RULE

The refactored code must run successfully.

A refactor that introduces syntax errors, import errors,
attribute errors, name errors, or behavioural regressions
is considered INVALID even if it improves maintainability.

OUTPUT CONTRACT (HIGHEST PRIORITY)

Return VALID JSON ONLY.

{{
  "refactored_code": "<python source code>"
}}

Forbidden:
- markdown
- code fences
- explanations
- notes
- apologies
- examples
- html
- xml
- yaml
- surrounding text

The FIRST character of your response must be {{
The LAST character of your response must be }}

If you output anything outside the JSON object, your response is invalid.
"""

def create_recommendations_prompt(file_content:str, cognitive_score: int,cyclomatic_score:int,
                  halstead_volume: float,loc: int,mi: float,cbo: float,
                  lcom:float,final_complex_score: float,final_maintain_score:float):
     return f"""
You are a senior Python software engineer.

Analyze the supplied Python source code and generate exactly 5 IMPLEMENTABLE refactoring recommendations.

METRICS:

Cognitive Complexity: {cognitive_score}
Cyclomatic Complexity: {cyclomatic_score}
Halstead Volume: {halstead_volume}
LOC: {loc}
Maintainability Index: {mi}
CBO: {cbo}
LCOM: {lcom}

FINAL SCORES:

Complexity: {final_complex_score}
Maintainability: {final_maintain_score}

SOURCE CODE:

{file_content}

RULES:

1. Generate exactly 5 recommendations.
2. Recommendations must be concrete.
3. Recommendations must reference actual code.
4. Recommendations must be implementable.
5. Recommendations must target:
   - duplication
   - nesting
   - long methods
   - maintainability
   - complexity

DO NOT GENERATE:

- improve readability
- improve maintainability
- simplify code
- separate concerns
- use better design

GOOD EXAMPLES:

- Extract helper method find_member from borrow_book.
- Extract helper method find_book from return_book.
- Replace nested conditional in send_notifications using guard clauses.
- Move duplicated lookup logic into a shared helper method.

OUTPUT CONTRACT:

Return VALID JSON ONLY.

{{
  "recommendations": [
    "recommendation 1",
    "recommendation 2",
    "recommendation 3",
    "recommendation 4",
    "recommendation 5"
  ]
}}

DO NOT RETURN ANYTHING EXCEPT JSON.
"""

def prompt_retry_rec(current_ref_code: str ,original_code: str, complexity_score: float , maintainability_score: float, user_feedback: str):
   return f"""
You are a senior Python software engineer.
 
Generate exactly 5 refactoring recommendations.
 
CRITICAL PRIORITY:
 
USER FEEDBACK OVERRIDES EVERYTHING ELSE.
 
USER FEEDBACK:
 
{user_feedback}
 
ORIGINAL SOURCE CODE:
 
{original_code}
 
CURRENT REFACTORED CODE:
 
{current_ref_code}
 
CURRENT SCORES:
 
Complexity: {complexity_score}
Maintainability: {maintainability_score}
 
RULES:
 
1. Recommendations MUST satisfy user feedback.
2. Recommendations MUST preserve behaviour from the original source.
3. Recommendations MUST NOT remove functionality.
4. Recommendations MUST NOT remove classes from the original source.
5. Recommendations MUST NOT remove public methods from the original source.
6. If functionality was removed, recommendations must restore it.
7. Generate exactly 5 concrete recommendations.
 
OUTPUT CONTRACT:
 
Return VALID JSON ONLY.
 
{{
"recommendations": [
"recommendation 1",
"recommendation 2",
"recommendation 3",
"recommendation 4",
"recommendation 5"
]
}}
 
DO NOT RETURN ANYTHING EXCEPT JSON.
"""
    

def prompt_retry_ref(current_ref_code:str,og_code: str, recs: str, user_feedback:str):
    return f"""
You are a senior Python software engineer.

TASK:
Modify the current refactored code.

USER FEEDBACK:

{user_feedback}

RECOMMENDATIONS TO IMPLEMENT:

{recs}

ORIGINAL SOURCE CODE:

{og_code}

CURRENT REFACTORED CODE:

{current_ref_code}

MANDATORY RULES:

1. User feedback takes highest priority.
2. Implement ALL recommendations.
3. Preserve original behaviour.
4. Preserve all classes from the original source.
5. Preserve all public methods from the original source.
6. Restore any classes removed from the original source.
7. Restore any methods removed from the original source.
8. Reduce duplication.
9. Reduce nesting.
10. Improve maintainability.
11. Improve readability.
12. Reduce complexity where possible.

VERIFICATION CHECKLIST:

Before returning code verify:

- Every original class exists.
- Every original public method exists.
- User feedback has been implemented.
- All recommendations have been implemented.
- Behaviour remains equivalent.

FUNCTIONALITY PRESERVATION RULE

The refactored code must run successfully.

A refactor that introduces syntax errors, import errors,
attribute errors, name errors, or behavioural regressions
is considered INVALID even if it improves maintainability.

OUTPUT CONTRACT (HIGHEST PRIORITY)

Return VALID JSON ONLY.

{{
  "refactored_code": "<python source code>"
}}

Forbidden:
- markdown
- code fences
- explanations
- notes
- apologies
- examples
- html
- xml
- yaml
- surrounding text

The FIRST character of your response must be {{
The LAST character of your response must be }}

If you output anything outside the JSON object, your response is invalid.
"""

    
    

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
            "format":"json"
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
        
    result2 = json.loads(data2["response"])
    code = str(result2["refactored_code"])
    code = code.replace("```python", "")
    code = code.replace("```", "")
    code = code.replace("````python", "")
    code = code.strip()

    generated = datetime.now().date()
    
    res = await store_ref_results(analysis_id, recs, code, generated, db)
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
    
    #need to fetch the original code incase user wnted to go back or the model needs to know exact logic
    file_id = analysis_obj.file_id
    file_data = await fetch_file(file_id,analysis_obj.proj_id,db,user)
    og_code = get_file_content(file_data["file_path"])
    
    #getting prev ref 
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
    
    prompt_rec = prompt_retry_rec(code,og_code,complexity_score, maintainability_score, user_feedback)
    

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
    
    prompt_ref = prompt_retry_ref(code, og_code,recs,user_feedback)
    response2 = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt":prompt_ref,
            "stream":False,
            "format": "json"
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
     
    result2 = json.loads(data2["response"])
    code = str(result2["refactored_code"])
    code = code.replace("```python", "")
    code = code.replace("```", "")
    code = code.replace("````python", "")
    code = code.strip()
    
    
    generated = datetime.now().date()
    res = await update_ref_results(ref_id, recs, code, generated, db) #update exisitng entry instead of new records.
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
    try:
        ast_tree = ast.parse(refactored_code)
    except SyntaxError as e:
        raise HTTPException( status_code = 400, detail = f"Generated code is invalid python : {e} ")
    
    score_model = await analyze_source_code(ast_tree,proj_id,db,None,analysis_id)
    data.complexity_after = score_model["complexity_score"]
    data.maintainability_after = score_model["maintainability_score"]
    db.add(data)
    db.commit()
    return {"proj_id":proj_id, "analysis_id":analysis_id, "ref_id": refactor_id, "complexity_after":score_model["complexity_score"],
            "maintainability_after": score_model["maintainability_score"]}


#add a get refactored code? or smth    