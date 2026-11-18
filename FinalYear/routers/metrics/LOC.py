import ast

class LOC():
    def __init__(self,tree):
        self.tree = tree
        self.loc = 0
    
    def countLOC(self):
        for node in ast.walk(self.tree):
            if isinstance(node,ast.stmt):
                self.loc += 1
    
    def getLOC(self):
        return self.loc