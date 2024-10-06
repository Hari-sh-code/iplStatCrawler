import questionary
from .export_to_excel import export_to_excel
from .export_to_csv import export_to_csv


def export_to_file(collected_stats):
    """Export collected stats to a file."""

    # Validate the structure of collected_stats
    if not isinstance(collected_stats, list) or not all(isinstance(item, dict) for item in collected_stats):
        raise ValueError("collected_stats must be a list of dictionaries.")

    export_options = ["Excel", "CSV"]
    selected_format = questionary.select("Select the file format for export:", choices=export_options).ask()
    file_name = questionary.text("Enter the file name (without extension):").ask()

    if selected_format == "Excel":
        export_to_excel(collected_stats, file_name + ".xlsx")
    elif selected_format == "CSV":
        export_to_csv(collected_stats, file_name + ".csv")
