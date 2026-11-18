import ast

class LCOM(ast.NodeVisitor):
    
    def __init__(self,tree):
        self.tree = tree
        self.class_func_attr_dict = dict()
        self.current_func = None
        self.current_class=None
        
    def visit_ClassDef(self,node):
        if isinstance(node, ast.ClassDef):
            self.class_func_attr_dict[node.name]=dict()
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None
    
    
    #def collect_funcs(self):
        #for node in ast.walk(self.tree):
            #if isinstance(node, ast.FunctionDef):
                #self.func_attr_dict[node.name]=set()
    
    def visit_FunctionDef(self,node):
        self.current_func = node.name
        self.class_func_attr_dict[self.current_class][self.current_func]= set()
        self.generic_visit(node)
        self.current_func = None
        
    def visit_Attribute(self,node):
        if (
             isinstance(node.value, ast.Name) and
             node.value.id == "self" and
             self.current_class and
             self.current_func
             ):
             self.class_func_attr_dict[self.current_class][self.current_func].add(node.attr)
        self.generic_visit(node)
        
    def get_class_func_dict(self):
        return self.class_func_attr_dict
    
    def deriveLCOM(self):
        class_lcom = {}
        for Cls,methods in self.class_func_attr_dict.items(): #key value methods might be all keys together
            method_attrs = list(methods.values()) #getting their variable dict list
            P=0
            Q=0
            for i in range(len(method_attrs)):
                for j in range(i+1,len(method_attrs)):
                    if method_attrs[i].intersection(method_attrs[j]):
                        Q += 1
                    else:
                        P += 1
            
            class_lcom[Cls]= max( P - Q , 0)
        return class_lcom
    
    
            
            
        
    
        