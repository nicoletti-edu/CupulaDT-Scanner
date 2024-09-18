import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
from card_parser import handle_single_card_page, handle_multiple_results

# Common headers to bypass bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Referer': 'https://www.google.com',
}

def fetch_page(url, retries=3, wait_time=5):
    """Fetches a page with retry and exponential backoff in case of HTTP 429."""
    for attempt in range(retries):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 429:
            print(f"Received HTTP 429, waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            wait_time *= 2
        elif response.status_code == 200:
            return response
        else:
            print(f"Error: Status Code {response.status_code} for URL: {url}")
            return None
    print(f"Failed to fetch page after {retries} attempts.")
    return None

def search_card(card_name):
    """Search for a card and process the response."""
    encoded_card_name = quote(card_name)
    base_url = f"https://www.cupuladt.com.br/?view=ecom/itens&busca={encoded_card_name}"

    response = fetch_page(base_url)
    if not response:
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    if soup.find('div', class_='table-cards'):
        handle_single_card_page(soup)
    elif soup.find_all('div', class_='card-item'):
        handle_multiple_results(soup, HEADERS)  # Pass HEADERS to the function
    else:
        print(f"No results found for '{card_name}'.")
