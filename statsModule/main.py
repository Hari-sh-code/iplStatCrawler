import os
from collections import deque
import pandas as pd
import questionary
from data import list_categories, load_category_data, validate_excel_files
from player import collect_player_stats, suggest_player_names, filter_players_by_criteria
from history import save_search_history, display_search_history, track_selection_history
from ui import filter_categories, view_all_players, navigate_back_to_main, get_year_selection, get_row_count

def main():
    player_search_history = deque(maxlen=10)

    while True:
        base_path = '../scrapeModule/statsData'
        years = validate_excel_files(base_path, range(2008, 2024 + 1))

        if not years:
            print("No Excel files found for the specified years.")
            return

        selected_year = get_year_selection(years)
        excel_file = years[int(selected_year)]  # Convert selected_year back to int to access the dictionary
        categories = list_categories(excel_file)

        if not categories:
            print(f"No categories found in the file.")
            return

        selected_categories = filter_categories(categories)

        if not selected_categories:
            print("No categories selected.")
            return

        row_count = get_row_count()

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
                df = load_category_data(excel_file, selected_category)
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
                df = load_category_data(excel_file, selected_category)
                print(f"\nTop {row_count} players in category '{selected_category}':")
                top_players = df.head(row_count)
                print(top_players)
                collected_stats.append(top_players)

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
                df = load_category_data(excel_file, selected_category)
                view_all_players(df)

        filter_option = questionary.confirm("Would you like to filter players by specific criteria?",
                                            default=False).ask()
        if filter_option:
            for selected_category in selected_categories:
                df = load_category_data(excel_file, selected_category)
                filtered_df = filter_players_by_criteria(df)
                if not filtered_df.empty:
                    print(filtered_df)

        save_selection_option = questionary.confirm("Would you like to save your selection history to a file?", default=False).ask()
        if save_selection_option:
            track_selection_history(selection_history)

        display_search_history(player_search_history)

        save_history_option = questionary.confirm("Would you like to save the player search history to a file?",
                                                  default=False).ask()
        if save_history_option:
            save_search_history(player_search_history)

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
                    break
                except Exception as e:
                    print(f"An error occurred: {e}. Please try again.")

        if not navigate_back_to_main():
            break

if __name__ == '__main__':
    main()
