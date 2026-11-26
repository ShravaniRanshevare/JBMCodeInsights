from fastapi import FastAPI,APIRouter,Depends,HTTPException
from ..database import SessionLocal
from ..models import Users,Project,FileRef,Analysis,Metrics
from .auth import get_current_user
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from typing import Annotated
from pathlib import Path
from .metrics import cognitive_complexity_calculator,cyclomatic_complexity,LOC,maintainabilityIndex,halstead_vol,CBO,LCOM,maxNestingDepth,codesmells
import ast
import math

router = APIRouter ( prefix="/analyse" , tags = ["analyse"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

    
# class AnalyseDeets(BaseModel):
#     astTree: ast.Module
#     proj_id: int
#     file_path: str| None = None
#     source_code: 

    
def normalize_cognitive(score):
    max_expected = 150.0
    return min((score / max_expected) *100, 100.0)
    
def normalize_cyclomatic(score):
    max_expected = 50.0
    return min((score/max_expected)*100, 100.0)
    
def normalize_halstead(score):
    max_expected = 5000.0
    return min((score / max_expected) * 100, 100.0)
    
def normalize_loc(score):
    max_expected = 500.0
    return min((score / max_expected) * 100, 100.0)



    
def final_LCOM(lcom_score): #per class score based off of methods attrs even cbo was avg finally 
    return max(lcom_score.values()) if lcom_score else 0

    
def normalize_CBO(avg_cbo):
    if avg_cbo:
        cbo = min(avg_cbo/10,1) #higher score utna coupling
    else:
        cbo = 1
    cbo = 1 - cbo
    return cbo


    
def normalize_LCOM(avg_lcom):
    max_expected = 20.0
    lcom_ratio = min(avg_lcom/max_expected,1.0) #higher score utna lack of cohesion
    lcom = 1 - lcom_ratio
    return lcom

def normalize_MI(mi_score):
    mi_norm = min(mi_score/100,1)
    return mi_norm

def normalize_nesting(nesting):
    depth = min(nesting/10,1)
    depth = 1 - depth
    return depth

def calculate_scores(coco,cyclo,hv,loc):
    coco_score = normalize_cognitive(coco)
    cyclo_score = normalize_cyclomatic(cyclo)
    hv_score = normalize_halstead(hv)
    loc_score = normalize_loc(loc)
    
    final_score = final_score = (0.4*coco_score + 0.4*hv_score + 0.15*cyclo_score + 0.05*loc_score)
    final_score = round(final_score, 1)
    return final_score

def get_complexity_category(score):
    if score <= 20:
        return "Very Low"
    elif score <= 40:
        return "Low"
    elif score <= 60:
        return "Moderate"
    elif score <= 80:
        return "High"
    else:
        return "Very High"

def calculate_maintainability(mi,cbo,lcom,nesting):
    score = ((0.40*mi + 0.20*cbo + 0.20*lcom + 0.20*nesting ))*100
    return round(score,1)

def get_maintainability_category(score):
    if score <= 20:
        return "Very Poor"
    elif score <= 40:
        return "Poor"
    elif score <= 60:
        return "Moderate"
    elif score <= 80:
        return "Good"
    else:
        return "Excellent"
    

async def fetch_file(file_id: int,proj_id:int,db:db_dependency,user:user_dependency):
    if not user:
        return False
    proj_model = db.query(Project).filter(Project.user_id == user["id"]).filter(Project.id == proj_id).first()
    if not proj_model:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    file_model = db.query(FileRef).filter(FileRef.proj_id == proj_id).filter(FileRef.id == file_id).first()
    if not file_model:
        raise HTTPException(status_code=404, detail="No such file found to analyze")
    return {"id": file_model.id, "file_path": file_model.file_path}

def create_AST(file_path: str):
    tree = ast.parse(Path(file_path).read_text())
    return tree


async def store_Analysis_results(proj_id,file_id,final_Complex_score,final_Maintain_score,db: db_dependency):
    analysis_obj = Analysis(
        proj_id = proj_id,
        file_id = file_id,
        complexity_score = final_Complex_score,
        maintainability_score = final_Maintain_score,
        retries = 0) #update later after recommendations
    db.add(analysis_obj)
    db.commit()
    db.refresh(analysis_obj)
    return analysis_obj.id
    
async def store_Metrics_results(analysis_id,cognitive_score,cyclomatic_score,halstead_volume,loc,mi,cbo,lcom,nesting,db: db_dependency):
    metrics_obj = Metrics(
        analysis_id = analysis_id,
        cognitive_score = cognitive_score,
        cyclomatic_score = cyclomatic_score,
        halstead_volume = halstead_volume,
        loc = loc,
        maintainability_index = mi,
        cbo = cbo,
        lcom = lcom,
        depth = nesting)
    db.add(metrics_obj)
    db.commit()
    
def get_penalties(astTree):
    duplicates = codesmells.detect_duplicates(astTree)
    longmethod_detector = codesmells.LongMethodDetector()
    longmethod_detector.visit(astTree)
    long_penalties = longmethod_detector.get_penalty()
    godclass_detector = codesmells.GodClassDetector()
    godclass_detector.visit(astTree)
    god_penalties = godclass_detector.get_penalty()
    
    return (duplicates, long_penalties ,god_penalties)

    
async def analyze_source_code(astTree,proj_id,db:db_dependency,file_id = None, analysis_id=None): #since we cover 2 analysis for refactored and normal code one  so for refactored each retry belongs to one analysis 
    coco = cognitive_complexity_calculator.CognitiveComplexityCalculator()
    cyclo = cyclomatic_complexity.CyclomaticAnalyzer()
    HV = halstead_vol.HalsteadVolume()
    loc = LOC.LOC(astTree)
    cbo = CBO.CBO(astTree)
    lcom = LCOM.LCOM(astTree)
    nesting = maxNestingDepth.MaxNestingDepth()
    
    coco.visit(astTree)
    cyclo.visit(astTree)
    HV.visit(astTree)
    loc.countLOC()
    cbo.collect_classes()
    cbo.visit(astTree)
    lcom.visit(astTree)
    nesting.visit(astTree)
    
    
    coco_scores = coco.return_results()
    cyclo_scores = cyclo.return_results()
    
    totalCoco = sum(coco_scores.values())
    totalCyclo = sum(cyclo_scores.values())
    
    halstead_v = HV.get_halstead_vol()
    Lines_of_code = loc.getLOC()
    
    
    MI = maintainabilityIndex.MaintainabilityIndex(halstead_v,totalCyclo,Lines_of_code)
    mi_score = MI.getIndex()
    
    cbo_score = cbo.deriveCBO()
    lcom_score = lcom.deriveLCOM()
    lcom_score = final_LCOM(lcom_score) #one more step for lcom
    nesting = nesting.get_depth()
    print( mi_score, cbo_score,lcom_score,nesting)
    
    Final_cbo = normalize_CBO(cbo_score)
    Final_lcom = normalize_LCOM(lcom_score)
    Final_mi = normalize_MI(mi_score)
    Final_depth = normalize_nesting(nesting)
    
    
    
    #code smells penalties - additional factor added 
    dupes, long_penalty, god_penalty = get_penalties(astTree)
    penalty = min ((dupes+long_penalty+god_penalty),20)
    
    #proper score weights were decided as per research
    final_Complex_score = calculate_scores(totalCoco,totalCyclo,halstead_v,Lines_of_code)
    complex_category = get_complexity_category(final_Complex_score)
    final_Maintain_score = max((calculate_maintainability(Final_mi,Final_cbo,Final_lcom,Final_depth) - penalty) , 0)
    
    
    maintain_category = get_maintainability_category(final_Maintain_score)
    
    if file_id and analysis_id == None :
        #storing results
        analysis_id = await store_Analysis_results(proj_id,file_id,final_Complex_score,final_Maintain_score,db)
        await store_Metrics_results(analysis_id,totalCoco,totalCyclo,halstead_v,Lines_of_code,mi_score,cbo_score,lcom_score,nesting,db)
    
    
    
        score_model = {"file_id" : file_id,  #every analysis entry needs file path
                       "analysis_id": analysis_id,
                        "complexity_score" : final_Complex_score,
                       "complexity category": complex_category,
                       "maintainability_score" : final_Maintain_score,
                       "maintainability category": maintain_category,
                       "penalty score for code smells": penalty}
    else:
        score_model = {
            "analysis_id": analysis_id,
            "complexity_score" : final_Complex_score,
            "complexity category": complex_category,
            "maintainability_score" : final_Maintain_score,
            "maintainability category": maintain_category,
            "penalty score for code smells": penalty}
    
    return score_model
    
    

@router.get("/get_score/{proj_id}/{file_id}",status_code = status.HTTP_200_OK)
async def analyze(proj_id:int,file_id: int, db:db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Need to authenticate before you can proceed")
    file_data = await fetch_file(file_id,proj_id,db,user)
    file_id,file_path = file_data.values()
    astTree = create_AST(file_path)
    score_model = await analyze_source_code(astTree,proj_id,db,file_id,None)

    return score_model
    

#complexity lower the better
#maintainability the higher the better

@router.get("/{proj_id}/{file_id}/get-all-analysis", status_code = status.HTTP_200_OK)
async def get_all_analysis_file(proj_id:int , file_id:int, db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Need to authenticate before you can proceed")
    proj = ( db.query(Project).filter(Project.user_id==user["id"]).filter(Project.id==proj_id).first())
    if not proj:
        raise HTTPException(status_code=404, detail=" No such project")
    file_model = db.query(FileRef).filter(FileRef.proj_id == proj_id).filter(FileRef.id == file_id).first()
    if not file_model:
        raise HTTPException(status_code=404, detail="No such file found")
    list_analysis = db.query(Analysis).filter(Analysis.file_id==file_id).all()
    if not list_analysis:
        raise HTTPException(status_code=404, detail="No analysis exist in our insights")
    return [ {"id": analysis.id, "complexity_score": analysis.complexity_score, "maintainability_score": analysis.maintainability_score, "retries": analysis.retries}
              for analysis in list_analysis]

    
@router.delete("/{proj_id}/{analysis_id}/delete", status_code = status.HTTP_204_NO_CONTENT)
async def delete_analysis(proj_id: int, analysis_id:int, db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Need to authenticate before you can proceed")
    proj = ( db.query(Project).filter(Project.user_id==user["id"]).filter(Project.id==proj_id).first())
    if not proj:
        raise HTTPException(status_code=404, detail=" No such project")
    analysis_obj = db.get(Analysis).filter(Analysis.proj_id==proj_id).filter(Analysis.id == analysis_id).first()
    if not analysis_obj:
        raise HTTPException(status_code=404, detail=" No such analysis made")
    db.delete(analysis_obj)
    db.commit()
    return {"msg": "analysis deleted"}



@router.get("/dashboard/overview",status_code = status.HTTP_200_OK)
async def get_overview(db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401,detail="Need to authenticate before you can proceed")
    projects_list = (db.query(Project).filter(Project.user_id==user["id"]).filter(Project.id==proj_id).all())
    number_proj=0
    if projects_list:
        number_proj = len(projects_list)
    number_analysis = 0
    avg_complexity = 0.0
    total_complexity=0
    avg_maintainability = 0.0
    total_maintainability=0
    for proj in projects_list:
        res = (db.get(Analysis).filter(Analysis.proj_id==proj_id).all())
        proj_analysis = len(res)
        number_analysis += proj_analysis
        total_complexity += sum([ analysis.complexity_score for analysis in res])
        total_maintainability += sum([ analysis.maintainability_score for analysis in res])
    
    avg_complexity = round(total_complexity/number_analysis,1)
    avg_maintainability = round(total_maintainability/number_analysis,1)
    
    return {"projects": number_proj, "analysis done":number_analysis, "avg_complexity": avg_complexity, "avg_maintainability": avg_maintainability}
    

    