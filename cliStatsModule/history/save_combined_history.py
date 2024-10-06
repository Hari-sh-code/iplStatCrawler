import json
import os

def save_combined_history(history, filename="search_history.json"):
    """Save search history to a JSON file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as file:
        json.dump(history, file, indent=4)

    print(f"Search history saved to {filename}.")
