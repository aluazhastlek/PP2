import re
import json
from datetime import datetime


def parse_receipt(text):
    """
    Parse receipt text using regular expressions and return structured data.
    """

    # Extract prices 
    price_pattern = r'\d+[.,]\d{2}'
    prices_raw = re.findall(price_pattern, text)

    prices = []
    for p in prices_raw:
        p = p.replace(',', '.')
        prices.append(float(p))

    # Extract product names with prices 
    product_pattern = r'^\s*\d+\.\s*(.+?)\s+\d+[.,]\d{2}$'
    product_matches = re.findall(product_pattern, text, re.MULTILINE)

    products = []

    for i, name in enumerate(product_matches):
        if i < len(prices):
            products.append({
                "name": name.strip(),
                "price": prices[i]
            })

    # Extract total 
    total_pattern = r'(ИТОГО|TOTAL)[:\s]*([\d\s,\.]+)'
    total_match = re.search(total_pattern, text, re.IGNORECASE)

    if total_match:
        total_str = total_match.group(2)
        total_str = total_str.replace(' ', '').replace(',', '.')
        total_amount = float(total_str)
    else:
        total_amount = sum(prices)

    #  Extract date and time 
    datetime_pattern = r'(\d{2}[./]\d{2}[./]\d{4})\s*(\d{2}:\d{2}:\d{2})?'
    datetime_match = re.search(datetime_pattern, text)

    date_value = None
    time_value = None

    if datetime_match:
        date_value = datetime_match.group(1)
        time_value = datetime_match.group(2)

    #  Extract payment method 
    payment_pattern = r'(Cash|Card|Наличные|Карта|Банковская карта)'
    payment_match = re.search(payment_pattern, text, re.IGNORECASE)

    payment_method = payment_match.group(1) if payment_match else "Unknown"

    #  Build structured result 
    result = {
        "date": date_value,
        "time": time_value,
        "products": products,
        "total_amount": round(total_amount, 2),
        "payment_method": payment_method
    }

    return result


def main():

    try:
        with open("raw.txt", "r", encoding="utf-8") as file:
            receipt_text = file.read()

    except FileNotFoundError:
        print("Error: raw.txt file not found.")
        return

    parsed = parse_receipt(receipt_text)

    # JSON output to console
    print("=== JSON OUTPUT ===")
    json_output = json.dumps(parsed, ensure_ascii=False, indent=4)
    print(json_output)

    # Save JSON to file
    with open("parsed_receipt.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_output)

    # Create formatted receipt summary
    summary_lines = []
    summary_lines.append("=== RECEIPT SUMMARY ===")
    summary_lines.append(f"Date: {parsed['date']}")
    summary_lines.append(f"Time: {parsed['time']}")
    summary_lines.append(f"Payment method: {parsed['payment_method']}")
    summary_lines.append(f"Total: {parsed['total_amount']:.2f}")
    summary_lines.append("\nProducts:")

    for i, product in enumerate(parsed["products"], 1):
        summary_lines.append(f"{i}. {product['name']} — {product['price']:.2f}")

    summary_text = "\n".join(summary_lines)

    # Print summary
    print("\n" + summary_text)

    # Save summary to text file
    with open("receipt_summary.txt", "w", encoding="utf-8") as summary_file:
        summary_file.write(summary_text)

    print("\nFiles saved successfully:")
    print("parsed_receipt.json")
    print("receipt_summary.txt")


if __name__ == "__main__":
    main()