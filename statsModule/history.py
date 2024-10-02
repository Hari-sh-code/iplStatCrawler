def save_search_history(history, filename='search_history.txt'):
    with open(filename, 'w') as file:
        for index, name in enumerate(history, 1):
            file.write(f"{index}: {name}\n")
    print(f"Search history saved to {filename}.")

def display_search_history(history):
    if history:
        print("\nSearch History:")
        for index, name in enumerate(history, 1):
            print(f"{index}: {name}")
    else:
        print("No search history available.")

def track_selection_history(selected_options):
    print("\nYour selections:")
    for index, option in enumerate(selected_options, 1):
        print(f"{index}: {option}")

    with open('selection_history.txt', 'a') as file:
        file.write("\n".join(selected_options) + "\n")
    print("Selections saved to selection_history.txt.")
