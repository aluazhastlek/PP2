class Student:
    def __init__(self, name, year):
        # Constructor method that initializes object attributes
        self.name = name          # Instance variable: unique for each object
        self.year = year          # Instance variable: unique for each object

    def introduce(self):
        # Instance method that accesses object data using self
        return f"My name is {self.name} and I am in year {self.year}."


# Creating objects (instances of the class)
s1 = Student("Malika", 1)
s2 = Student("Alua", 2)

print(s1.introduce())
print(s2.introduce())