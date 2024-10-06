import questionary

def navigate_back_to_main():
    """Prompt user to navigate back to the main menu."""
    return questionary.confirm("Would you like to go back to the main menu?", default=True).ask()
