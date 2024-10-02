from fuzzywuzzy import process
import questionary

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

def filter_players_by_criteria(df):
    available_columns = df.columns.tolist()
    selected_columns = questionary.checkbox(
        "Select criteria to filter players:",
        choices=available_columns
    ).ask()

    filtered_df = df.copy()

    for column in selected_columns:
        min_value = questionary.text(f"Enter minimum value for '{column}' (or press Enter to skip):").ask()

        if min_value.isdigit():
            filtered_df = filtered_df[filtered_df[column] >= int(min_value)]
        elif min_value:
            print(f"Invalid input for '{column}', skipping.")

    return filtered_df
