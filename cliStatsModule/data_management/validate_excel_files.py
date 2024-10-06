import os

def validate_excel_files(base_path, years):
    """Validate the existence of Excel files for the given years."""
    years = {year: os.path.join(base_path, f"{year}_stats.xlsx") for year in years}
    return {year: path for year, path in years.items() if os.path.exists(path)}
