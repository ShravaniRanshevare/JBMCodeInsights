import ast
from routers.metrics.LOC import LOC
from pathlib import Path


def test_0_loc():
    code = ""
    tree = ast.parse(code)
    loc = LOC(tree)
    loc.countLOC()
    res = loc.getLOC()
    assert res == 0
    
def test_23_loc():
    code = """
class Calculator:

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return None
        return a / b

    def average(self, numbers):
        total = 0

        for num in numbers:
            total += num

        return total / len(numbers)

    def maximum(self, numbers):
        return max(numbers)

    def minimum(self, numbers):
        return min(numbers)


calc = Calculator()

nums = [1, 2, 3, 4, 5]

print(calc.average(nums))
"""
    tree = ast.parse(code)
    loc = LOC(tree)
    loc.countLOC()
    res = loc.getLOC()
    assert res == 23
    
def test_50_loc():
    code = """
class Student:

    def __init__(self, name, grades):
        self.name = name
        self.grades = grades

    def get_average(self):
        return sum(self.grades) / len(self.grades)

    def get_highest(self):
        return max(self.grades)

    def get_lowest(self):
        return min(self.grades)


class School:

    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def calculate_averages(self):

        averages = {}

        for student in self.students:
            averages[student.name] = student.get_average()

        return averages

    def display_report(self):

        for student in self.students:

            print("Name:", student.name)
            print("Average:", student.get_average())
            print("Highest:", student.get_highest())
            print("Lowest:", student.get_lowest())
            print()


school = School()

school.add_student(
    Student("Alice", [80, 90, 85])
)

school.add_student(
    Student("Bob", [70, 75, 80])
)

school.add_student(
    Student("Charlie", [90, 95, 100])
)

school.display_report()

for i in range(10):
    print(i)

for i in range(10):
    print(i * 2)

for i in range(10):
    print(i * 3)

for i in range(10):
    print(i * 4)

for i in range(10):
    print(i * 5)

for i in range(10):
    print(i * 6)

for i in range(10):
    print(i * 7)

for i in range(10):
    print(i * 8)

for i in range(10):
    print(i * 9)
"""
    tree = ast.parse(code)
    loc = LOC(tree)
    loc.countLOC()
    res = loc.getLOC()
    assert res == 50
    

def test_LOC_high():
    code = Path("/Users/shravaniranshevare1806/Library/CloudStorage/OneDrive-UniversityofHertfordshire/progam/AI/BigFile-testLOC.py").read_text()
    tree = ast.parse(code)
    loc = LOC(tree)
    loc.countLOC()
    res = loc.getLOC()
    assert res > 100
    