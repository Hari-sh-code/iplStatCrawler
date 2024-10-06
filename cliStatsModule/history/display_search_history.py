import json
import os

def display_search_history(filename="search_history.json"):
    """Display search history from a JSON file."""
    if not os.path.exists(filename):
        print("No search history found.")
        return

    with open(filename, 'r') as file:
        history = json.load(file)

    if history:
        print("\nSearch History:")
        for entry in history:
            print(entry)
    else:
        print("Search history is empty.")
