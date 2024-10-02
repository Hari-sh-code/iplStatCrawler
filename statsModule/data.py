import pandas as pd
import os

def list_categories(excel_file):
    xls = pd.ExcelFile(excel_file)
    return xls.sheet_names

def load_category_data(excel_file, category):
    return pd.read_excel(excel_file, sheet_name=category)

def validate_excel_files(base_path, years):
    years = {year: os.path.join(base_path, f"{year}_stats.xlsx") for year in years}
    return {year: path for year, path in years.items() if os.path.exists(path)}
