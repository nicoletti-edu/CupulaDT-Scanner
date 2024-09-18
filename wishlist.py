import json

def load_wishlist(filename):
    """Loads card names from a JSON wishlist file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            wishlist = json.load(file)
            return wishlist.get('cards', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading wishlist: {e}")
        return []
