import pandas as pd

def load_category_data(excel_file, category):
    """Load data from a specified category (sheet) in the Excel file."""
    return pd.read_excel(excel_file, sheet_name=category)
