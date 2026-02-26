# ============================================
# 1) Generator that generates squares up to N
# ============================================

def square_generator(n):
    # Yields the square of numbers from 0 to n
    for i in range(n + 1):
        yield i * i


print("Squares up to N:")
N = int(input("Enter N: "))
for value in square_generator(N):
    print(value)


# ======================================================
# 2) Generator to print even numbers between 0 and n
# ======================================================

def even_numbers(n):
    # Yields even numbers from 0 to n
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


print("\nEven numbers:")
n = int(input("Enter n: "))
print(",".join(str(num) for num in even_numbers(n)))


# ==================================================================
# 3) Generator for numbers divisible by both 3 and 4 (0 to n)
# ==================================================================

def divisible_by_3_and_4(n):
    # Yields numbers divisible by both 3 and 4 (i.e., divisible by 12)
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


print("\nNumbers divisible by 3 and 4:")
n = int(input("Enter n: "))
for num in divisible_by_3_and_4(n):
    print(num)


# ==========================================================
# 4) Generator squares from a to b
# ==========================================================

def squares(a, b):
    # Yields squares of numbers from a to b
    for i in range(a, b + 1):
        yield i * i


print("\nSquares from a to b:")
a = int(input("Enter a: "))
b = int(input("Enter b: "))
for value in squares(a, b):
    print(value)


# ==========================================================
# 5) Generator that returns numbers from n down to 0
# ==========================================================

def countdown(n):
    # Yields numbers from n down to 0
    while n >= 0:
        yield n
        n -= 1


print("\nCountdown:")
n = int(input("Enter n: "))
for value in countdown(n):
    print(value)