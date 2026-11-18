import ast
from routers.metrics.maxNestingDepth import MaxNestingDepth

def test_0_depth():
    code = """
def hello():
    print("hi")
    """
    tree = ast.parse(code)
    depth = MaxNestingDepth()
    depth.visit(tree)
    res = depth.get_depth()
    assert res == 0
    
    
def test_1_depth():
    code = """
if a+b==10:
    print ('10')
"""
    tree = ast.parse(code)
    depth = MaxNestingDepth()
    depth.visit(tree)
    res = depth.get_depth()
    assert res == 1
    

def test_3_depth():
    code = """
if a:
    if b:
        if c:
            pass
"""
    tree = ast.parse(code)
    depth = MaxNestingDepth()
    depth.visit(tree)
    res = depth.get_depth()
    assert res == 3
    
def test_loop_if_depth():
    code = """
for i in range(10):
    if i > 5:
        print(i)
"""
    tree = ast.parse(code)
    depth = MaxNestingDepth()
    depth.visit(tree)
    res = depth.get_depth()
    assert res == 2

def test_mixed_depth():
    code = """
while x:

    if y:

        for i in range(10):

            if z:
                pass
                """
    tree = ast.parse(code)
    depth = MaxNestingDepth()
    depth.visit(tree)
    res = depth.get_depth()
    assert res == 4

def test_monster_nesting_depth():
    code = """
if a:
    if b:
        if c:
            if d:
                if e:
                    pass
                    """
    tree = ast.parse(code)
    depth = MaxNestingDepth()
    depth.visit(tree)
    res = depth.get_depth()
    assert res == 5





