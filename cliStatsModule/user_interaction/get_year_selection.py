import questionary

def get_year_selection(years):
    return questionary.select(
        "Select a year:",
        choices=[str(year) for year in years.keys()]  # Ensure years are strings
    ).ask()
