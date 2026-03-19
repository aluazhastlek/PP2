from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map()
squared = list(map(lambda x: x ** 2, numbers))
print("Squared numbers:", squared)

# filter()
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)

# reduce()
total = reduce(lambda a, b: a + b, numbers)
print("Reduced sum:", total)

# Other built-in functions
print("Length:", len(numbers))
print("Sum:", sum(numbers))
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))