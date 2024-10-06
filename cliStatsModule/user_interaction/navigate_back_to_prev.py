import questionary

def navigate_back_to_prev():
    """Prompt user to navigate back to the previous menu."""
    return questionary.confirm("Would you like to go back to the previous menu?", default=False).ask()