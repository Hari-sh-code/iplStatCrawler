import questionary

def get_year_selection(years):
    return questionary.select(
        "Select a year:",
        choices=[str(year) for year in years.keys()]
    ).ask()

def get_row_count():
    return int(questionary.select(
        "How many rows would you like to display?",
        choices=[str(i) for i in range(1, 21)],
        default='5'
    ).ask())

def filter_categories(categories):
    stripped_categories = [category.strip() for category in categories]
    return questionary.checkbox(
        "Select categories to include:",
        choices=stripped_categories,
        default=stripped_categories[0] if stripped_categories else None
    ).ask()

def view_all_players(df):
    print("\nAll players in category:")
    print(df)

def navigate_back_to_main():
    return questionary.confirm("Would you like to go back to the main menu?", default=True).ask()