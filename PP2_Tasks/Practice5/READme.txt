Practice 5 – Python Regular Expressions (RegEx)

Objective

    The goal of this practice is to learn how to use regular expressions in Python with the re module.
    This project demonstrates how to search, match, extract, and replace text patterns.
    A practical task in this project is parsing a receipt file (raw.txt) and extracting structured information from it.

Project Structure
    Practice5/
    │
    ├── receipt_parser.py
    ├── raw.txt
    └── README.md

    receipt_parser.py – Python script that parses receipt data using regular expressions

    raw.txt – raw receipt text used for parsing

    README.md – project documentation

Technologies Used

    Python 3

    re module (Python Regular Expressions)

    json module

    datetime module

Regular Expression Features Demonstrated

    This project demonstrates the following regex concepts:

    Metacharacters (., *, +, ?, ^, $)

    Character classes ([])

    Quantifiers ({n}, {n,m})

    Special sequences (\d, \s, \w)

    Pattern matching with:

    re.search()

    re.findall()

    re.split()

    re.sub()

    Regex flags such as re.MULTILINE and re.IGNORECASE

Receipt Parsing Tasks

    The script performs the following operations on the receipt text:

        Extracts all product prices

        Extracts product names

        Calculates the total amount

        Extracts date and time

        Detects the payment method

        Creates structured output in JSON format

Example Output

    Example JSON result:

        {
            "date": "04.03.2026",
            "time": "14:35:20",
            "products": [
                {
                    "name": "Milk",
                    "price": 2.50
                },
                {
                    "name": "Bread",
                    "price": 1.20
                }
            ],
            "total_amount": 3.70,
            "payment_method": "Card"
        }
How to Run the Program

    Make sure Python is installed.

    Place the receipt text inside raw.txt.

    Run the script:

        python receipt_parser.py

    The program will parse the receipt and display structured data in the console.

Resources

    W3Schools Python RegEx Tutorial
    https://www.w3schools.com/python/python_regex.asp
