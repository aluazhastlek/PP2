# sort data by a field 
products = [
    ("notebook", 1200),
    ("pen", 150),
    ("laptop", 350000),
    ("mouse", 8000),
]

# Sort by price (2nd element)
by_price = sorted(products, key=lambda item: item[1])
print("Example 4 (sorted by price):", by_price)

# Sort by name length (1st element length)
by_name_length = sorted(products, key=lambda item: len(item[0]))
print("Example 4 (sorted by name length):", by_name_length)
