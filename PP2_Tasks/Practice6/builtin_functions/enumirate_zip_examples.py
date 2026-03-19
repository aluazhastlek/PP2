names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

# enumerate()
print("Using enumerate():")
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

# zip()
print("\nUsing zip():")
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# Type checking
value1 = "123"
value2 = 45.67
value3 = [1, 2, 3]

print("\nType checking:")
print(value1, "->", type(value1))
print(value2, "->", type(value2))
print(value3, "->", type(value3))

# Type conversions
int_value = int(value1)
float_value = float(value1)
str_value = str(value2)
list_to_tuple = tuple(value3)

print("\nType conversions:")
print("String to int:", int_value)
print("String to float:", float_value)
print("Float to string:", str_value)
print("List to tuple:", list_to_tuple)