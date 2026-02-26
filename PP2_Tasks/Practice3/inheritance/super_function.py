# Example 2: Using super() to call parent constructor

class Employee(Person):
    def __init__(self, name, position):
        super().__init__(name)   # Calls parent class constructor
        self.position = position

    def info(self):
        return f"{self.name} works as a {self.position}."


e = Employee("Dias", "Developer")
print(e.info())