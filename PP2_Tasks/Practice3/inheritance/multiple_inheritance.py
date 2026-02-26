# Example 4: Multiple inheritance

class CanCode:
    def skill(self):
        return "Can write code."


class CanTeach:
    def teach(self):
        return "Can teach students."


class Mentor(CanCode, CanTeach):
    # Inherits from two parent classes
    pass


mentor = Mentor()
print(mentor.skill())
print(mentor.teach())