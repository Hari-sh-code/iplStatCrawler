import questionary
import pandas as pd

def filter_players_by_criteria(df):
    """Prompt user to filter players based on specified criteria."""
    available_columns = df.columns.tolist()  # Get available columns from the DataFrame

    if len(available_columns) < 2:
        print("Not enough columns available to filter by.")
        return df  # Return original DataFrame if there are not enough columns

    # Exclude the second column
    filtered_columns = available_columns[:1] + available_columns[2:]  # Keep the first column and all columns after the second

    selected_columns = questionary.checkbox(
        "Select criteria to filter players (excluding the second column):",
        choices=filtered_columns
    ).ask()

    if not selected_columns:
        print("No criteria selected. Returning the original DataFrame.")
        return df  # Return original DataFrame if no selection is made

    filtered_df = df  # Initialize filtered DataFrame

    for col in selected_columns:
        if pd.api.types.is_numeric_dtype(df[col]):  # Check if the column is numeric
            min_value = questionary.text(f"Enter minimum value for '{col}' (leave empty for no minimum):").ask()
            max_value = questionary.text(f"Enter maximum value for '{col}' (leave empty for no maximum):").ask()

            if min_value:
                filtered_df = filtered_df[filtered_df[col] >= float(min_value)]
            if max_value:
                filtered_df = filtered_df[filtered_df[col] <= float(max_value)]
        else:
            filter_value = questionary.text(f"Enter value to filter for '{col}':").ask()
            if filter_value:
                filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(filter_value, case=False, na=False)]

    if not filtered_df.empty:
        print("\nFiltered Results:")
        print(filtered_df)
    else:
        print("No players match the selected criteria.")

    return filtered_df
