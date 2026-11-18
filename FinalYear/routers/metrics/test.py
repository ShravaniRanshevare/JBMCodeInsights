import sys

sys.path.append(
    "/Users/shravaniranshevare1806/Library/CloudStorage/OneDrive-UniversityofHertfordshire/FinalYear/routers"
)
from metrics import cognitive_complexity_calculator, cyclomatic_complexity, halstead_vol,LOC,maintainabilityIndex,CBO,LCOM
import ast

content = None
with open("/Users/shravaniranshevare1806/Library/CloudStorage/OneDrive-UniversityofHertfordshire/FinalYear/routers/metrics/worksheet5.py","r") as fr:
    content = fr.read()
    
def final_LCOM(lcom_score): #per class score based off of methods attrs even cbo was avg finally 
    avg_lcom = (sum(lcom_score.values())/len(lcom_score) 
                )
    return avg_lcom
    
def normalize_CBO(avg_cbo):
    cbo_norm = min(avg_cbo/10,1)
    cbo_score = 1 - cbo_norm
    return cbo_score #higher score cz of this is good


    
def normalize_LCOM(avg_lcom):
    lcom_norm = min(avg_lcom/10,1)
    lcom_score = 1 - lcom_norm
    return lcom_score #same

def normalize_MI(mi_score):
    mi_norm = mi_score/100
    return mi_norm


astTree = ast.parse(content)
coco = cognitive_complexity_calculator.CognitiveComplexityCalculator()
cyclo = cyclomatic_complexity.CyclomaticAnalyzer()
HV = halstead_vol.HalsteadVolume()
loc = LOC.LOC(astTree)
cbo = CBO.CBO(astTree)
lcom = LCOM.LCOM(astTree)

coco.visit(astTree)
cyclo.visit(astTree)
HV.visit(astTree)
cbo.collect_classes()
cbo.visit(astTree)
lcom.visit(astTree)

co = coco.return_results()
cyc = cyclo.return_results()

totalCoco = sum(co.values())
totalCyclo= sum(cyc.values())

loc.countLOC()
hv = HV.get_halstead_vol()
Loc = loc.getLOC()
MI = maintainabilityIndex.MaintainabilityIndex(hv,totalCyclo,Loc)
mi = MI.getIndex() #requires cc and coco ka sum so wait
cbo_score = cbo.deriveCBO()
lcom_score = lcom.deriveLCOM()
LCOM = final_LCOM(lcom_score) #one more step for lcom
    
Final_cbo = normalize_CBO(cbo_score)
Final_lcom = normalize_LCOM(LCOM)
Final_mi = normalize_MI(mi)

print("co , cyc, loc, hv, Loc, MI,cbo,lcom", co,cyc,Loc,hv, Final_mi,Final_cbo,Final_lcom)
