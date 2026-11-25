import ast #cbo class level metric

class CBO(ast.NodeVisitor):
    def __init__(self,tree):
        self.tree = tree
        self.class_coupling = dict()
        self.current_class=None
        self.class_names= set()
        
    def collect_classes(self): #first run this to collect all classes
        for node in ast.walk(self.tree):
            if isinstance(node,ast.ClassDef):
                self.class_names.add(node.name)
        
    def visit_ClassDef(self,node): 
        self.current_class = node.name
        self.class_coupling[node.name]= set()
        self.generic_visit(node)
        self.current_class = None
        
        
    def visit_Call(self,node):
        if (
            self.current_class and
            isinstance(node.func, ast.Name) and
            node.func.id != self.current_class and
            node.func.id in self.class_names
            ):
            self.class_coupling[self.current_class].add(node.func.id)
        self.generic_visit(node)
        
    def get_class_coupling(self):
        return self.class_coupling
    
    def deriveCBO(self):
        totalCbo=0
        for key in self.class_coupling:
            cbo = len(self.class_coupling[key])
            totalCbo += cbo
        if totalCbo:
            return (totalCbo/len(self.class_coupling))
        else:
            return 0

