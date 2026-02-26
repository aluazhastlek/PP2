
class Laptop:
    warranty_years = 2   # Class variable (shared across all instances)

    def __init__(self, brand, price):
        self.brand = brand    # Instance variable
        self.price = price    # Instance variable


l1 = Laptop("Dell", 350000)
l2 = Laptop("Apple", 900000)

# Accessing class variable
print(Laptop.warranty_years)

# Overriding class variable for one specific instance
l2.warranty_years = 3

print(l1.warranty_years)  # Still uses class variable (2)
print(l2.warranty_years)  # Uses instance-level value (3)