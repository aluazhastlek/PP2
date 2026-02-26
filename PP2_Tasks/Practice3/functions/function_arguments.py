def stats(numbers):
    # numbers is a list argument
    # Returns sum, average, and max as a tuple
    total = sum(numbers)
    avg = total / len(numbers) if len(numbers) > 0 else 0
    biggest = max(numbers) if len(numbers) > 0 else None
    return total, avg, biggest

nums = [10, 20, 30, 5]
total, avg, biggest = stats(nums)
print("Sum:", total)
print("Average:", avg)
print("Max:", biggest)
