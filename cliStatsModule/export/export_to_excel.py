import pandas as pd

def export_to_excel(collected_stats, filename="exported_data.xlsx"):
    """Export collected stats to an Excel file."""
    with pd.ExcelWriter(filename) as writer:
        for idx, df in enumerate(collected_stats):
            df.to_excel(writer, sheet_name=f"Sheet{idx + 1}", index=False)
    print(f"Data exported to {filename} successfully.")
