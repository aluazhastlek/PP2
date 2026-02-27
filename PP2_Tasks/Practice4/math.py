import math

# 1) Convert degree to radian
degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)
print("Output radian:", round(radian, 6))


# 2) Area of a trapezoid
height = float(input("\nHeight: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

trapezoid_area = 0.5 * (base1 + base2) * height
print("Expected Output:", trapezoid_area)


# 3) Area of regular polygon
n = int(input("\nInput number of sides: "))
s = float(input("Input the length of a side: "))

polygon_area = (n * s**2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(polygon_area))


# 4) Area of a parallelogram
base = float(input("\nLength of base: "))
height_para = float(input("Height of parallelogram: "))

parallelogram_area = base * height_para
print("Expected Output:", parallelogram_area)