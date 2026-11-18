import ast
from routers.metrics.halstead_vol import HalsteadVolume
from pathlib import Path

def test_HV_small():
    code = """
a = b+c
"""
    tree = ast.parse(code)
    hv = HalsteadVolume()
    hv.visit(tree)
    vol = hv.get_halstead_vol()
    assert vol > 10
    assert vol < 12
    

def test_repeated_operands():
    code = """
x = x + 1
"""
    tree = ast.parse(code)
    hv = HalsteadVolume()
    hv.visit(tree)
    vol = hv.get_halstead_vol()
    assert vol == 10

def test_for():
    code = """
for i in range(5):
    total += 1
"""
    tree = ast.parse(code)
    hv = HalsteadVolume()
    hv.visit(tree)
    vol = hv.get_halstead_vol()
    assert vol > 18
    assert vol < 20
    
def test_if():
    code = """
if x > 0:
    x = x+1
"""
    tree = ast.parse(code)
    hv = HalsteadVolume()
    hv.visit(tree)
    vol = hv.get_halstead_vol()
    assert vol > 24
    assert vol < 26
    
    
    