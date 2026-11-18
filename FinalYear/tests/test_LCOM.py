import ast
import pprint
from routers.metrics.LCOM import LCOM


def final_LCOM(lcom_score): #per class score based off of methods attrs even cbo was avg finally 
    return max(lcom_score.values()) if lcom_score else 0

def test_goodLCOM():
    code = """
class User:
    def __init__(self):
        self.name = ""

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def clear_name(self):
        self.name = ""
    """
    tree = ast.parse(code)
    lcom = LCOM(tree)
    lcom.visit(tree)
    class_lcom = lcom.deriveLCOM()
    res = final_LCOM(class_lcom)
    assert res == 0
    
def test_moderateLCOM():
    code = """
class Employee:

    def __init__(self):
        self.name = ""
        self.salary = 0

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_salary(self, salary):
        self.salary = salary

    def get_salary(self):
        return self.salary
        """
    tree = ast.parse(code)
    lcom = LCOM(tree)
    lcom.visit(tree)
    class_lcom = lcom.deriveLCOM()
    res = final_LCOM(class_lcom)
    assert res < 3
    assert res > -1
    
def test_terribleLCOM():
    code = """
class Utility:

    def login(self):
        username = "admin"

    def send_email(self):
        email = "x@test.com"

    def generate_report(self):
        report = []

    def connect_database(self):
        host = "localhost"

    def calculate_salary(self):
        salary = 5000
        """
    tree = ast.parse(code)
    lcom = LCOM(tree)
    lcom.visit(tree)
    class_lcom = lcom.deriveLCOM()
    res = final_LCOM(class_lcom)
    assert res == 10
    
def test_HIGH():
    code = """
class System:

    def login(self):
        self.users = []

    def generate_report(self):
        self.reports = []

    def send_email(self):
        self.emails = []

    def backup(self):
        self.backups = []

    def process_order(self):
        self.orders = []

    def calculate_payroll(self):
        self.payroll = []
        """
    tree = ast.parse(code)
    lcom = LCOM(tree)
    lcom.visit(tree)
    class_lcom = lcom.deriveLCOM()
    res = final_LCOM(class_lcom)
    assert res == 15