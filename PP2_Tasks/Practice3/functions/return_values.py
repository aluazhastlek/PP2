#1
def rectangle_area(width, height):
    # Returns the area of a rectangle
    return width * height

w = 5
h = 3
area = rectangle_area(w, h)   # function call + return value stored in a variable
print("Area:", area)

#2
def count(text):                     # Defines a function to count uppercase and lowercase letters
    upper = 0                        # Initializes uppercase counter
    lower = 0                        # Initializes lowercase counter
    for char in text:                # Iterates through each character in the text
        if char.isupper():           # Checks if the character is uppercase
            upper += 1               # Increments uppercase counter
        elif char.islower():         # Checks if the character is lowercase
            lower += 1               # Increments lowercase counter
    return upper, lower              # Returns both counters as a tuple

text = input()                       # Takes input text from the user
upper, lower = count(text)           # Calls the function and unpacks the result
print("Number of upper case characters :", upper)  # Prints number of uppercase letters
print("Number of lower case characters :", lower)  # Prints number of lowercase letters
