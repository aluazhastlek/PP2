# keep only items that match a rule (even numbers)
nums = [3, 10, 15, 22, 7, 40, 41]
evens = list(filter(lambda n: n % 2 == 0, nums))
print("Example 3 (filter evens):", evens)

# Keep only words longer than 5 characters
words = ["apple", "banana", "kiwi", "cherry", "pear", "strawberry"]
long_words = list(filter(lambda w: len(w) > 5, words))
print("Example 3 (filter long words):", long_words)