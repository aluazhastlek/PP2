#1
def greeting(firstname):        # Defines a function named greeting with one parameter
   print('Hello,', firstname)  # Prints a greeting with the given name

fname = input()                # Takes input from the user and stores it in fname
greeting(fname)                # Calls the function using the input as an argument

#2
def greet(name, city="Astana"):
    # name is a positional argument
    # city is a default argument (used if not provided)
    print(f"Hello, {name}! You are from {city}.")

greet("Alua")                 # uses default city
greet("Malika", "Almaty")     # overrides default city
