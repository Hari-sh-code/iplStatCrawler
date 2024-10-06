import questionary

def get_row_count():
    """Prompt user to specify how many rows to display."""
    return int(questionary.select("How many rows would you like to display (Max. 60)?", choices=[str(i) for i in range(1, 61)],
                                  default='5').ask())
