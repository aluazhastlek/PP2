# apply discount)
prices = [1000, 2500, 3990, 12000]
discounted = list(map(lambda p: int(p * 0.9), prices))  # 10% off
print("Example 2 (map):", discounted)

# transformation: Celsius -> Fahrenheit
celsius = [0, 10, 20, 30]
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))
print("Example 2 (C->F):", fahrenheit)
