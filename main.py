from wishlist import load_wishlist
from fetcher import search_card
from utils import initialize_csv

def process_wishlist(filename):
    """Processes each card from the wishlist file."""
    card_names = load_wishlist(filename)
    if not card_names:
        print("No card names found in the wishlist.")
        return

    for card_name in card_names:
        print(f"\nSearching for card: {card_name}")
        search_card(card_name)

if __name__ == "__main__":
    # Initialize the CSV log file
    initialize_csv()

    # Process the wishlist
    process_wishlist("wishlist.json")
