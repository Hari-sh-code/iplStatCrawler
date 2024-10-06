import questionary

def filter_categories(categories):
    """Prompt user to select categories for analysis."""
    stripped_categories = [category.strip() for category in categories]
    return questionary.checkbox("Select categories to include:", choices=stripped_categories).ask()
