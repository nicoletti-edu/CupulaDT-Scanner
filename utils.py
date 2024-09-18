import re
import csv
from datetime import datetime

def extract_card_data(row):
    """Extracts data for each card including edition, language, condition, extras, stock, and price."""
    try:
        edition = re.sub(r'Edição\s+', '', row.find('div', class_='tooltip-item').text.strip())
        language = re.sub(r'Idioma\s+', '', row.find_all('div', class_='tooltip-item')[1].text.strip())

        # Handle missing or incorrect condition safely
        try:
            condition_element = row.find_all('div', class_='tooltip-item')[2]
            condition_match = re.search(r'(NM|LP|MP|HP|SP|EX)', condition_element.text.strip())
            condition = condition_match.group() if condition_match else "Unknown"
        except (IndexError, AttributeError):
            condition = "Unknown"

        # Extract extras field, remove unnecessary "Extras" label and newlines
        try:
            extras_element = row.find('div', class_='card-extras')
            extras = extras_element.text.strip().replace('Extras\n', '') if extras_element else "-"
            extras = extras.replace('\n', ', ')  # Handle any extra newlines inside the field
        except (IndexError, AttributeError):
            extras = "-"

        # Handle missing stock safely
        try:
            stock_raw = row.find_all('div', class_='tooltip-item')[4].text.strip()
            stock_cleaned = re.sub(r'\D+', '', stock_raw)  # Remove everything that's not a digit
            stock = int(stock_cleaned) if stock_cleaned else 0
        except (IndexError, AttributeError):
            stock = 0

        # Extract price
        price = re.sub(r'Preço\s+', '', row.find('div', class_='card-preco').text.strip())

        return {
            "edition": edition,
            "language": language,
            "condition": condition,
            "extras": extras,
            "stock": stock,
            "price": price
        }
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None



def log_price_data(card_name, edition, language, condition, extras, stock, price, log_file="price_log.csv"):
    """Logs the card price data into a CSV file with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [timestamp, card_name, edition, language, condition, extras, stock, price]

    # Write to CSV
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    print(f"Logged data for {card_name}: {price} at {timestamp}")

# Optional: Add header if the file doesn't exist yet
def initialize_csv(log_file="price_log.csv"):
    """Creates the CSV file and writes the header if it doesn't already exist."""
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Card Name', 'Edition', 'Language', 'Condition', 'Extras', 'Stock', 'Price'])

def fetch_min_price(soup):
    """Fetches the minimum price from the card page based on available stock."""
    table_rows = soup.find_all('div', class_='table-cards-row')
    prices = []

    for row in table_rows:
        try:
            # Extract stock value and ensure it's available
            stock_raw = row.find_all('div', class_='tooltip-item')[4].text.strip()
            stock_cleaned = re.sub(r'\D+', '', stock_raw)  # Remove everything that's not a digit
            stock = int(stock_cleaned) if stock_cleaned else 0

            if stock > 0:
                # Extract price and clean it up
                price_raw = row.find('div', class_='card-preco').get_text(separator=" ").strip()
                price_cleaned = re.sub(r'Preço\s+', '', price_raw)
                price_numeric = re.sub(r'[^\d,]', '', price_cleaned).replace(',', '.')
                
                if price_numeric:
                    prices.append(float(price_numeric))
        except (IndexError, AttributeError):
            # Handle any missing data safely by skipping this entry
            continue

    if prices:
        return f"R$ {min(prices):.2f}"
    return "Price not available"
