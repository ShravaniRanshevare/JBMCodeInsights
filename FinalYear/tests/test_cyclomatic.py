import ast
from pathlib import Path
from routers.metrics.cyclomatic_complexity import CyclomaticAnalyzer
import pprint


def test_1_cyclo():
    code = """
def hello():
    print('x') """
    tree = ast.parse(code)
    cyclo = CyclomaticAnalyzer()
    cyclo.visit(tree)
    res = sum(cyclo.return_results().values())
    assert res == 1
    
def test_worksheet3():
    code = Path("/Users/shravaniranshevare1806/Library/CloudStorage/OneDrive-UniversityofHertfordshire/progam/AI/worksheet3.py").read_text()
    tree = ast.parse(code)
    cyclo = CyclomaticAnalyzer()
    cyclo.visit(tree)
    vals = cyclo.return_results().values()
    pprint.pprint(vals)
    res = sum(vals) #45
    assert res == 45
    
def test_worksheet6():
    code = Path("/Users/shravaniranshevare1806/Library/CloudStorage/OneDrive-UniversityofHertfordshire/progam/AI/worksheet6.py").read_text()
    tree = ast.parse(code)
    cyclo = CyclomaticAnalyzer()
    cyclo.visit(tree)
    vals = cyclo.return_results().values()
    pprint.pprint(vals)
    res = sum(vals) #64
    assert res == 64
    
def test_if_and_bool():

    code = """
def f(a,b):
    if a and b:
        pass
"""
    tree = ast.parse(code)
    cyclo = CyclomaticAnalyzer()
    cyclo.visit(tree)
    res = sum(cyclo.return_results().values()) #3
    assert res == 3
    