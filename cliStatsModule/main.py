from user_interaction.navigate_back_to_prev import navigate_back_to_prev
from data_management.list_categories import list_categories
from data_management.load_category_data import load_category_data
from data_management.validate_excel_files import validate_excel_files
from user_interaction.get_year_selection import get_year_selection
from user_interaction.filter_categories import filter_categories
from user_interaction.view_all_players import view_all_players
from user_interaction.navigate_back_to_main import navigate_back_to_main
from player.collect_player_stats import collect_player_stats
from player.suggest_player_names import suggest_player_names
from player.filter_players_by_criteria import filter_players_by_criteria
from collections import deque
import pandas as pd
import questionary

def main():
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
            print("No categories found in the file.")
            return

        selected_categories = filter_categories(categories)

        if not selected_categories:
            print("No categories selected.")
            return

        collected_stats = []  # Initialize collected_stats for all data
        has_displayed_data = False  # Flag to check if data has been displayed
        row_counts = {}  # Dictionary to store row counts for each category

        while True:
            # First round options
            if not has_displayed_data:
                display_option = questionary.select(
                    "How would you like to display the data?",
                    choices=["Row count", "Display all category", "Search player", "Filter category"]
                ).ask()
            else:  # Add Exit option in the second round
                display_option = questionary.select(
                    "How would you like to display the data?",
                    choices=["Row count", "Display all category", "Search player", "Filter category", "Exit"]
                ).ask()

            if display_option == "Row count":
                # Get row count for each selected category
                for selected_category in selected_categories:
                    row_count = int(questionary.select(f"How many rows would you like to display for category '{selected_category}' (Max. 60)?",
                                                       choices=[str(i) for i in range(1, 61)],
                                                       default='5').ask())
                    row_counts[selected_category] = row_count  # Store row count for the category

                    print(f"Total number of rows selected for category '{selected_category}': {row_count}")
                    df = load_category_data(excel_file, selected_category)
                    top_players = df.head(row_count)
                    print(f"\nTop {row_count} players in category '{selected_category}':")
                    print(top_players)

                    # Convert DataFrame to a list of dictionaries and append
                    collected_stats.append(top_players.to_dict(orient='records'))

                has_displayed_data = True  # Set flag to indicate data has been displayed

            elif display_option == "Display all category":
                for selected_category in selected_categories:
                    df = load_category_data(excel_file, selected_category)
                    view_all_players(df)

                    # Convert DataFrame to a list of dictionaries and append
                    collected_stats.append(df.to_dict(orient='records'))

                has_displayed_data = True  # Set flag to indicate data has been displayed

            elif display_option == "Search player":
                player_name = questionary.text("Enter the player's name:").ask()

                # Collect player name suggestions from all selected categories
                all_suggestions = set()
                for selected_category in selected_categories:
                    df = load_category_data(excel_file, selected_category)
                    suggestions = suggest_player_names(df, player_name)
                    all_suggestions.update(suggestions)

                if all_suggestions:
                    selected_suggestion = questionary.select("Select a suggested player:", choices=list(all_suggestions)).ask()

                    # Collect stats for the selected player from all categories
                    for selected_category in selected_categories:
                        df = load_category_data(excel_file, selected_category)
                        player_stats = collect_player_stats(df, selected_suggestion, row_counts.get(selected_category, 5))  # Use stored row count or default to 5
                        if player_stats is not None:
                            print(f"\nStats for player '{selected_suggestion}' in category '{selected_category}':")
                            print(player_stats)

                            # Convert player_stats DataFrame to a list of dictionaries and append
                            collected_stats.append(player_stats.to_dict(orient='records'))

                else:
                    print(f"No suggestions found for player '{player_name}'.")

            elif display_option == "Filter category":
                for selected_category in selected_categories:
                    df = load_category_data(excel_file, selected_category)
                    filtered_df = filter_players_by_criteria(df)

                    # Convert filtered DataFrame to a list of dictionaries and append
                    collected_stats.append(filtered_df.to_dict(orient='records'))

                has_displayed_data = True  # Set flag to indicate data has been displayed

            elif display_option == "Exit":
                break  # Exit the loop

            # Check if the user wants to navigate back to the prev menu
            if not navigate_back_to_prev():
                break

        # Prompt to navigate back to the main menu or exit
        if not navigate_back_to_main():
            break

if __name__ == "__main__":
    main()
