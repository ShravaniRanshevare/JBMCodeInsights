import ast
from routers.metrics.CBO import CBO


def test_zero_cbo():
    code = """
class Users:
    def __init__(self):
        self.ontop = 'me'
    
    def get_name(self):
        return self.ontop
"""
    tree = ast.parse(code)
    cbo = CBO(tree)
    cbo.collect_classes()
    cbo.visit(tree)
    res = cbo.deriveCBO()
    assert res == 0
    
def test_one_cbo():
    code = """
class Engine:
    pass

class Car:
    def __init__(self):
        self.engine = Engine()
"""
    tree = ast.parse(code)
    cbo = CBO(tree)
    cbo.collect_classes()
    cbo.visit(tree)
    res = cbo.deriveCBO() #0.5
    assert res > 0.4
    assert res < 0.6
    

def test_multiple_dependencies():
    code = """
class A:
    pass

class B:
    pass

class C:
    pass

class D:
    pass


class Controller:

    def __init__(self):
        self.a = A()
        self.b = B()
        self.c = C()
        self.d = D()
"""
    tree = ast.parse(code)
    cbo = CBO(tree)
    cbo.collect_classes()
    cbo.visit(tree)
    res = cbo.deriveCBO() #0.8
    assert res > 0.7
    assert res < 0.9
    
def test_high_cbo():
    code = """
class User:
    pass

class Product:
    pass

class Order:
    pass

class Payment:
    pass

class Inventory:
    pass

class EmailService:
    pass


class Monster:

    def __init__(self):
        self.user = User()
        self.product = Product()
        self.order = Order()
        self.payment = Payment()
        self.inventory = Inventory()
        self.email = EmailService()
"""
    tree = ast.parse(code)
    cbo = CBO(tree)
    cbo.collect_classes()
    cbo.visit(tree)
    res = cbo.deriveCBO() #0.875
    assert res > 0.7
    assert res < 0.9
