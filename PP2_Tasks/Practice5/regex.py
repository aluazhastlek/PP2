import re

# 1. Match 'a' followed by zero or more 'b's
# 'b*' означает: ноль или более 'b'
print("1. Match 'a' followed by zero or more 'b's")
pattern1 = r"ab*"
test1 = ["a", "ab", "abb", "b", "ba"]
for s in test1:
    if re.fullmatch(pattern1, s):  # проверяем полное совпадение со строкой
        print(f"Match: {s}")
print("-" * 50)

# 2. Match 'a' followed by 2 to 3 'b's
# 'b{2,3}' означает: 2 или 3 буквы 'b' подряд
print("2. Match 'a' followed by 2 to 3 'b's")
pattern2 = r"ab{2,3}"
test2 = ["ab", "abb", "abbb", "abbbb"]
for s in test2:
    if re.fullmatch(pattern2, s):
        print(f"Match: {s}")
print("-" * 50)

# 3. Find sequences of lowercase letters joined with underscore
# [a-z]+ – одна или более маленьких букв
# (?:_[a-z]+)+ – одно или несколько вхождений: "_" + буквы
print("3. Find sequences of lowercase letters joined with underscore")
pattern3 = r"[a-z]+(?:_[a-z]+)+"
text3 = "hello_world test_case python_regex notMatched Example"
matches3 = re.findall(pattern3, text3)  # находим все совпадения
print(matches3)
print("-" * 50)

# 4. Find sequences of one uppercase letter followed by lowercase letters
# [A-Z] – одна заглавная
# [a-z]+ – одна или более маленьких
print("4. Find sequences of one uppercase letter followed by lowercase letters")
pattern4 = r"[A-Z][a-z]+"
text4 = "Hello World Python regex Test123"
matches4 = re.findall(pattern4, text4)
print(matches4)
print("-" * 50)

# 5. Match 'a' followed by anything, ending with 'b'
# '.*' – любое количество любых символов
print("5. Match 'a' followed by anything, ending with 'b'")
pattern5 = r"a.*b"
test5 = ["ab", "a123b", "acb", "b"]
for s in test5:
    if re.fullmatch(pattern5, s):
        print(f"Match: {s}")
print("-" * 50)

# 6. Replace all spaces, commas, or dots with colon
# [ ,\.] – пробел, запятая или точка
print("6. Replace all spaces, commas, or dots with colon")
text6 = "Hello, world. This is regex"
new_text6 = re.sub(r"[ ,\.]", ":", text6)  # заменяем все совпадения на ':'
print(new_text6)
print("-" * 50)

# 7. Convert snake_case to camelCase
# '_([a-z])' – находим символ после '_' и делаем его заглавным
print("7. Convert snake_case to camelCase")
text7 = "this_is_snake_case"
camel_case7 = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), text7)
print(camel_case7)
print("-" * 50)

# 8. Split string at uppercase letters
# '[A-Z][a-z]*' – заглавная буква + ноль или больше маленьких
print("8. Split string at uppercase letters")
text8 = "SplitAtUpperCaseLetters"
result8 = re.findall(r'[A-Z][a-z]*', text8)
print(result8)
print("-" * 50)

# 9. Insert spaces before capital letters
# '([A-Z])' – захватываем каждую заглавную букву
# ' \1' – вставляем пробел перед ней
print("9. Insert spaces before capital letters")
text9 = "HelloWorldThisIsRegex"
spaced9 = re.sub(r"([A-Z])", r" \1", text9).strip()  # strip убирает пробел в начале
print(spaced9)
print("-" * 50)

# 10. Convert camelCase to snake_case
# '([A-Z])' – находим заглавные буквы
# '_\1' – ставим перед ними '_', потом всё в lower()
print("10. Convert camelCase to snake_case")
text10 = "thisIsCamelCase"
snake_case10 = re.sub(r'([A-Z])', r'_\1', text10).lower()
print(snake_case10)
print("-" * 50)