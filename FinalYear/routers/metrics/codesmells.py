import ast
from collections import Counter

def detect_duplicates(tree):
    nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr):
            nodes.append(ast.dump(node))
    counts = Counter(nodes)
    
    duplicates = sum( c - 1 for c in counts.values() if c>1)
    return duplicates


class LongMethodDetector(ast.NodeVisitor):
    def __init__(self):
        self.long_methods = []
    
    def visit_FunctionDef(self,node):
        if ( hasattr(node,"end_linono") and node.end_lineno):
            length = (node.end_lineno - node.lineno)
            if length > 30:
                self.long_methods.append( (node.name,length))
            
        self.generic_visit(node)
    
    def get_penalty(self):
        total = 0
        for meth,leng in self.long_methods:
            if leng> 50:
                total += 8
            elif leng> 30:
                total += 5
        
        return total
#nesting depth already there
#variable name is tricky 
        
class GodClassDetector(ast.NodeVisitor):
    def __init__(self):
        self.matches = []
        
    def visit_ClassDef(self,node):
        method_count = sum( isinstance(n,ast.FunctionDef) for n in node.body)
        if method_count >10:
            self.matches.append(node.name)
            
    def get_penalty(self):
        if len(self.matches) > 10:
            return 8
        else:
            return 0
            