import ast

class CognitiveComplexityCalculator(ast.NodeVisitor):
    def __init__(self):
        self.complexity_score=0
        self.nesting=0
        self.current_function=None
        self.operator = None
        self.results= {}
        
    def handle_nesting(self,node):
        self.complexity_score += 1 + self.nesting
        self.nesting += 1
        self.generic_visit(node)
        self.nesting -= 1
        
    def visit_For(self,node):
        self.handle_nesting(node)
    
    def visit_If(self,node):
        self.visit(node.test)
        self.complexity_score += 1 + self.nesting
        self.nesting += 1
        for stmt in node.body:
            self.visit(stmt)
        self.nesting -= 1
        
        if (len(node.orelse) == 1 and isinstance(node.orelse[0],ast.If)):
            self.visit(node.orelse[0])
        else:
            self.nesting += 1
            for stmt in node.orelse:
                self.visit(stmt)
            self.nesting -= 1
        #if it has children this node then uk itss nested and u can add additional
    
    def visit_Match(self,node):
        self.handle_nesting(node)
    
    def visit_While(self,node):
        self.visit(node.test)
        self.handle_nesting(node)
    
    def visit_Try(self,node):
        self.handle_nesting(node)
        
    def visit_ExceptHandler(self,node):
        self.handle_nesting(node)
    
    #recursion ? operators if a &b +1 but if a&b&c if new op  still +1 and nested left too
    def visit_FunctionDef(self,node):
        
        
        old_function = self.current_function
        old_score = self.complexity_score
        old_nesting = self.nesting
        
        
        self.current_function = node.name
        self.complexity_score = 0
        self.nesting=0
        self.generic_visit(node)
        
        function_complexity = self.complexity_score
        self.results[node.name] = function_complexity
        self.complexity_score = old_score
        self.nesting = old_nesting
            
        self.current_function= old_function #now if u define another function sindie smth thats here too
        
    
    def visit_Call(self,node):
        if (
            isinstance(node.func,ast.Name) and
            node.func.id == self.current_function and
            node.func.id != "print"
            ):
            
            self.complexity_score += 1
        self.generic_visit(node)
    
    def visit_Continue(self,node):
        self.complexity_score += 1
        
    
    def visit_Break(self,node):
        self.complexity_score += 1
    
    
    def visit_BoolOp(self,node):
        self.complexity_score += len(node.values) - 1
        self.generic_visit(node) #lets add nested (and b) or (c and d) later
    
    def visit_Lambda(self,node): #lambda has no score 
        self.nesting += 1
        self.generic_visit(node)
        self.nesting -=1
        
    def visit_IfExp(self,node):
        self.complexity_score += 1 + self.nesting
        self.generic_visit(node)
        
    def visit_ListComp(self,node):
        self.complexity_score += 1
        for gen in node.generators:
            self.complexity_score += 1
            if gen.ifs:
                self.complexity_score += len(gen.ifs)
        self.generic_visit(node)
               
    def return_results(self):
        return self.results
        
        
        
        
    #maybe per node u llok at its children and if for loop if kitne hai utna additional fir genericvisit
    #for operators look at BoolOp node check all nodes
    #for call node +1 recursion node.func.id == current_function
            
    