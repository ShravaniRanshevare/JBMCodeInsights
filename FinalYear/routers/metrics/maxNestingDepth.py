import ast

class MaxNestingDepth(ast.NodeVisitor):
    def __init__(self):
        self.current_depth = 0
        self.max_depth = 0
    
    def visit_nested(self,node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth,self.current_depth)
        
        self.generic_visit(node)
        
        self.current_depth -= 1
        
    def visit_If(self,node):
        self.visit_nested(node)
        
    def visit_For(self,node):
        self.visit_nested(node)
        
    def visit_While(self,node):
        self.visit_nested(node)
    
    def visit_Try(self,node):
        self.visit_nested(node)
        
    def visit_With(self,node):
        self.visit_nested(node)
        
    def get_depth(self):
        return self.max_depth
    