#cyclomatic - function head, if elif , for , no nesting baaki sab same hi hai  measure = D + 1 so totalscore + 1
import ast
class CyclomaticAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.cyclomatic_score = 1
        self.results = {}
    
    
    def handle_scoring(self,node):
        self.cyclomatic_score += 1
        self.generic_visit(node)
        
    def visit_FunctionDef(self,node):
        old = self.cyclomatic_score
        self.cyclomatic_score = 1
        self.generic_visit(node)
        function_complexity = self.cyclomatic_score
        self.results[node.name] = function_complexity
        self.cyclomatic_score = old
        
    def visit_If(self,node):
        self.handle_scoring(node)
    
    def visit_For(self,node):
        self.handle_scoring(node)
    
    def visit_While(self,node):
        self.handle_scoring(node)
    
    
    def visit_ExceptHandler(self,node):
        self.handle_scoring(node)
        
    def visit_Try(self,node):
        self.handle_scoring(node)
    
    def visit_BoolOp(self,node):
        self.cyclomatic_score += len(node.values) - 1
        self.generic_visit(node)
    
    def visit_Match(self,node):
        self.handle_scoring(node)
        
    def visit_ListComp(self,node):

        for gen in node.generators:
            self.cyclomatic_score += 1
            if gen.ifs:
                self.cyclomatic_score += len(gen.ifs)
        self.generic_visit(node)
        
    def visit_IfExp(self,node):
        self.cyclomatic_score += 1
        self.generic_visit(node)
    
    def return_results(self):
        return self.results
    
    