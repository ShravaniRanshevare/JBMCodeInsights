import ast
from pathlib import Path
from routers.metrics.cognitive_complexity_calculator import CognitiveComplexityCalculator

def test_zero_cognitive_complexity():
    code = """
def hello():
    print('hi')"""
    
    tree = ast.parse(code)
    coco = CognitiveComplexityCalculator()
    coco.visit(tree)
    res = coco.return_results()
    res = sum(res.values())
    
    assert res == 0
    
    
def test_worksheet_3():
    code = Path("/Users/shravaniranshevare1806/Library/CloudStorage/OneDrive-UniversityofHertfordshire/progam/AI/worksheet3.py").read_text()
    tree = ast.parse(code)
    coco = CognitiveComplexityCalculator()
    coco.visit(tree)
    res = coco.return_results()
     #43
    res = sum(res.values())
    print(res)
    assert res==43
    
    
def test_worksheet_6():
    code = Path("/Users/shravaniranshevare1806/Library/CloudStorage/OneDrive-UniversityofHertfordshire/progam/AI/worksheet6.py").read_text()
    tree = ast.parse(code)
    coco = CognitiveComplexityCalculator()
    coco.visit(tree)
    res = coco.return_results()
    res = sum(res.values())
    print(res) #58
    assert res==58
    
    
def test_if_and_bool():

    code = """
def f(a,b):
    if a and b:
        pass
"""
    tree = ast.parse(code)
    cyclo = CognitiveComplexityCalculator()
    cyclo.visit(tree)
    res = sum(cyclo.return_results().values()) #2
    assert res == 2