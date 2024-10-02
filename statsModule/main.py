import pandas as pd
import os
import questionary
from fuzzywuzzy import process
from collections import deque


def list_categories(excel_file):
    xls = pd.ExcelFile(excel_file)
    return xls.sheet_names


def collect_player_stats(df, player_name, row_count):
    player_stats = df[df['PLAYER'].str.contains(player_name, case=False, na=False)]

    if player_stats.empty:
        print(f"No stats found for player '{player_name}'.")
        return None
    else:
        return player_stats.head(row_count)


def suggest_player_names(df, player_name):
    players = df['PLAYER'].unique()
    suggestions = process.extract(player_name, players, limit=5)
    return [name for name, score in suggestions if score > 50]


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


def filter_players_by_criteria(df):
    available_columns = df.columns.tolist()

    selected_columns = questionary.checkbox(
        "Select criteria to filter players:",
        choices=available_columns
    ).ask()

    filtered_df = df.copy()  # Start with a copy of the original DataFrame

    for column in selected_columns:
        min_value = questionary.text(f"Enter minimum value for '{column}' (or press Enter to skip):").ask()

        if min_value.isdigit():
            filtered_df = filtered_df[filtered_df[column] >= int(min_value)]
        elif min_value:
            print(f"Invalid input for '{column}', skipping.")

    if not filtered_df.empty:
        print("\nFiltered players:")
        print(filtered_df)
    else:
        print("No players match the specified criteria.")


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


def navigate_back_to_main():
    return questionary.confirm("Would you like to go back to the main menu?", default=True).ask()


def main():
    player_search_history = deque(maxlen=10)

    while True:
        base_path = 'scrapeModule/statsData'
        years = {str(year): os.path.join(base_path, f"{year}_stats.xlsx") for year in range(2008, 2024 + 1)}
        years = {year: path for year, path in years.items() if os.path.exists(path)}

        if not years:
            print("No Excel files found for the specified years.")
            return

        selected_year = questionary.select(
            "Select a year:",
            choices=list(years.keys())
        ).ask()

        excel_file = years[selected_year]
        categories = list_categories(excel_file)
        if not categories:
            print(f"No categories found in the file.")
            return

        selected_categories = filter_categories(categories)

        if not selected_categories:
            print("No categories selected.")
            return

        row_count = int(questionary.select(
            "How many rows would you like to display?",
            choices=[str(i) for i in range(1, 21)],
            default='5'
        ).ask())

        # Track selected options but don't save yet
        selection_history = [selected_year] + selected_categories + [str(row_count)]
        print("\nYour selections:")
        for index, option in enumerate(selection_history, 1):
            print(f"{index}: {option}")

        player_search = questionary.confirm(
            "Would you like to search stats for a particular player?",
            default=False
        ).ask()

        collected_stats = []
        if player_search:
            player_name = questionary.text("Enter the player's name:").ask()
            player_search_history.append(player_name)

            for selected_category in selected_categories:
                df = pd.read_excel(excel_file, sheet_name=selected_category)
                suggestions = suggest_player_names(df, player_name)

                if suggestions:
                    print("Did you mean one of these players?")
                    selected_suggestion = questionary.select(
                        "Select a suggested player:",
                        choices=suggestions
                    ).ask()
                    player_stats = collect_player_stats(df, selected_suggestion, row_count)
                    if player_stats is not None:
                        collected_stats.append(player_stats)
                else:
                    print(f"No suggestions available for '{player_name}' in category '{selected_category}'.")
        else:
            for selected_category in selected_categories:
                df = pd.read_excel(excel_file, sheet_name=selected_category)
                print(f"\nTop {row_count} players in category '{selected_category}':")
                top_players = df.head(row_count)
                print(top_players)
                collected_stats.append(top_players)

        # Perform sorting if needed
        if collected_stats:
            sort_option = questionary.confirm("Would you like to sort the displayed stats?", default=False).ask()
            if sort_option:
                df_to_sort = pd.concat(collected_stats)

                sort_column = questionary.select(
                    "Select a column to sort by:",
                    choices=df_to_sort.columns.tolist()
                ).ask()

                sort_order = questionary.select(
                    "Select sort order:",
                    choices=["Ascending", "Descending"]
                ).ask()

                sorted_df = df_to_sort.sort_values(by=sort_column, ascending=(sort_order == "Ascending"))
                print(sorted_df.head(row_count))

        view_all_players_option = questionary.confirm("Would you like to view all players in a category?",
                                                      default=False).ask()
        if view_all_players_option:
            for selected_category in selected_categories:
                df = pd.read_excel(excel_file, sheet_name=selected_category)
                view_all_players(df)

        filter_option = questionary.confirm("Would you like to filter players by specific criteria?",
                                            default=False).ask()
        if filter_option:
            for selected_category in selected_categories:
                df = pd.read_excel(excel_file, sheet_name=selected_category)
                filter_players_by_criteria(df)

        # Ask the user if they want to save the selection history
        save_selection_option = questionary.confirm("Would you like to save your selection history to a file?", default=False).ask()
        if save_selection_option:
            track_selection_history(selection_history)

        # Display search history
        display_search_history(player_search_history)

        # Ask the user if they want to save the player search history to a file
        save_history_option = questionary.confirm("Would you like to save the player search history to a file?",
                                                  default=False).ask()
        if save_history_option:
            save_search_history(player_search_history)

        # Export to CSV with error handling
        if questionary.confirm("Would you like to export the displayed stats to a CSV file?", default=False).ask():
            while True:
                export_path = questionary.text("Enter the export file path (include filename):").ask()
                if not export_path.endswith('.csv'):
                    print("Please provide a valid CSV file name with the '.csv' extension.")
                    continue

                try:
                    df_to_export = pd.concat(collected_stats)
                    df_to_export.to_csv(export_path, index=False)
                    print(f"Stats exported to {export_path}")
                    break  # Exit the loop on successful export
                except Exception as e:
                    print(f"An error occurred: {e}. Please try again.")

        if not navigate_back_to_main():
            break


if __name__ == '__main__':
    main()
