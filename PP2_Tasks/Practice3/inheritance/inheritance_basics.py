# Example 1: Basic parent-child relationship

class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, my name is {self.name}."


class Teacher(Person):
    # Inherits all attributes and methods from Person
    pass


t = Teacher("Aigerim")
print(t.greet())