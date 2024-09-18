import re
import requests
from bs4 import BeautifulSoup
from utils import extract_card_data, fetch_min_price, log_price_data

def handle_single_card_page(soup):
    """Handles a single card page by extracting editions and prices."""
    card_name = soup.find('div', class_='nome_en_cards').text.strip()
    print(f"\nCard: {card_name}")
    
    table_rows = soup.find_all('div', class_='table-cards-row')
    
    for row in table_rows:
        edition_data = extract_card_data(row)
        if edition_data:
            log_price_data(
                card_name, 
                edition_data['edition'], 
                edition_data['language'], 
                edition_data['condition'], 
                edition_data['extras'], 
                edition_data['stock'], 
                edition_data['price']
            )

def handle_multiple_results(soup, headers):
    """Handles a page with multiple card results and prints out details, including the price."""
    results = soup.find_all('div', class_='card-item')
    print("Found multiple cards. Listing the available cards:")
    
    for result in results:
        title = result.find('div', class_='title').text.strip()
        link = result.find('a')['href']
        full_link = f"https://www.cupuladt.com.br{link}"

        # Fetch the individual card page using headers to bypass anti-bot measures
        card_page_response = requests.get(full_link, headers=headers)
        if card_page_response.status_code == 200:
            card_page_soup = BeautifulSoup(card_page_response.content, 'html.parser')

            # Extract edition, language, condition, stock, and extras from the individual card page
            table_rows = card_page_soup.find_all('div', class_='table-cards-row')
            for row in table_rows:
                edition_data = extract_card_data(row)
                if edition_data:
                    log_price_data(
                        title, 
                        edition_data['edition'], 
                        edition_data['language'], 
                        edition_data['condition'], 
                        edition_data['extras'], 
                        edition_data['stock'], 
                        edition_data['price']
                    )
