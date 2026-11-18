import ast
import math
#halstead volume = N*log(n) N = total operators+operands and n = unique operators+operands

class HalsteadVolume(ast.NodeVisitor):
    def __init__(self):
        self.totaloperators = 0
        self.totalOperands = 0
        self.uniqueoperators = set()
        self.uniqueOperands = set()
    
    def add_operator(self, op):
        self.totaloperators += 1
        self.uniqueoperators.add(op)
        
    
    def bin_check(self,node):
        if type(node.op) == ast.Add:
            return "+"
        elif type(node.op) == ast.Sub:
            return "-"
        elif type(node.op) == ast.Mult:
            return "*"
        elif type(node.op) == ast.Div:
            return "/"
        elif type(node.op) == ast.FloorDiv:
            return "//"
        elif type(node.op) == ast.Mod:
            return "%"
        elif type(node.op) == ast.Pow:
            return "**"
        else:
            return "unknownbinop"
    
    def bool_check(self,node):
        if type(node.op) == ast.And:
            return "and"
        elif type(node.op) == ast.Or:
            return "or"
        else:
            return "unknownboolop"
    
    def unary_check(self,node):
        if type(node.op) == ast.Not:
            return "not"
        elif type(node.op) == ast.USub:
            return "usub"
        elif type(node.op) == ast.UAdd:
            return "uadd"
        elif type(node.op) == ast.Invert:
            return "invert"
        else:
            return "unknownunary"
        
    def aug_check(self,node):
        if type(node.op) == ast.Add:
            return "+="
        elif type(node.op) == ast.Sub:
            return "-="
        elif type(node.op) == ast.Mult:
            return "*="
        elif type(node.op) == ast.Div:
            return "/="
        
    def compare_check(self,node):
        if type(node.ops[0]) == ast.Eq:
            return "=="
        elif type(node.ops[0]) == ast.NotEq:
            return "!="
        elif type(node.ops[0]) == ast.Lt:
            return "<"
        elif type(node.ops[0]) == ast.LtE:
            return "<="
        elif type(node.ops[0]) == ast.Gt:
            return ">"
        elif type(node.ops[0]) == ast.GtE:
            return ">="
        elif type(node.ops[0]) == ast.Is:
            return "is"
        elif type(node.ops[0]) == ast.IsNot:
            return "is not"
        elif type(node.ops[0]) == ast.In:
            return "in"
        elif type(node.ops[0]) == ast.NotIn:
            return "not in"
        else:
            return "unknowncompare"
    
    
            
#visit node check if it comes in operators category if yes that score maintain a set of operators encountered since for unique
    def visit_If(self,node):
        self.add_operator("if")
        self.generic_visit(node)
    
    def visit_For(self,node):
        self.add_operator("for")
        self.generic_visit(node)
    
    def visit_While(self,node):
        self.add_operator("while")
        self.generic_visit(node)
    
    def visit_Assign(self,node): # = 
        self.add_operator("=")
        self.generic_visit(node)
    
    def visit_AugAssign(self,node): # x += 1
        op = self.aug_check(node)
        self.add_operator(op)
        self.generic_visit(node)
    
    def visit_BinOp(self,node):
        op = self.bin_check(node)
        self.add_operator(op)
        self.generic_visit(node)
            
    def visit_BoolOp(self,node):
        
        op = self.bool_check(node)
        self.add_operator(op)
        self.generic_visit(node)
    
    def visit_UnaryOp(self,node):
        op = self.unary_check(node)
        self.add_operator(op)
        self.generic_visit(node)
    
    def visit_Compare(self,node):
        op = self.compare_check(node)
        self.add_operator(op)
        self.generic_visit(node)
            
    def visit_Name(self,node): #variable x total etc when assigned variable is used
        self.totalOperands += 1
        if node.id not in self.uniqueOperands:
            self.uniqueOperands.add(node.id)
        self.generic_visit(node)
        
        
    def visit_Constant(self,node): #when x = 101 is assigned 
        self.totalOperands += 1
        if node.value not in self.uniqueOperands:
            self.uniqueOperands.add(str(node.value))
        self.generic_visit(node)
        
    def get_halstead_vol(self):
        N = self.totaloperators+ self.totalOperands
        n = len(self.uniqueoperators) + len(self.uniqueOperands)
        if n <= 0:
            return 0
        return N*math.log2(n)
    
    
    
    
    