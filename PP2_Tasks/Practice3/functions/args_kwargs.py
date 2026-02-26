#1
def add_all(*args):
    # *args collects extra positional arguments into a tuple
    # Example: add_all(1, 2, 3) -> args = (1, 2, 3)
    total = 0
    for n in args:
        total += n
    return total

print(add_all(1, 2, 3))       # 6
print(add_all(10, 5))         # 15
print(add_all())              # 0

#2
def build_profile(**kwargs):
    """
    Creates a user profile using keyword arguments.
    Returns a dictionary containing all provided fields.
    Example: build_profile(name="Alua", age=18) -> {"name": "Alua", "age": 18}
    """
    # **kwargs collects keyword arguments into a dictionary
    profile = {}
    for key, value in kwargs.items():
        profile[key] = value
    return profile

user = build_profile(name="Malika", university="NU", year=1, city="Astana")
print(user)