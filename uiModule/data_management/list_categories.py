import pandas as pd

def list_categories(excel_file):
    """List all categories (sheets) in the Excel file."""
    xls = pd.ExcelFile(excel_file)
    return xls.sheet_names
