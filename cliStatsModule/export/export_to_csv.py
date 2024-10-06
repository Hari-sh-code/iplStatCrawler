import pandas as pd

def export_to_csv(data, file_name):
    """Export collected stats to a CSV file."""
    # Check if data is in the correct format
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        df = pd.DataFrame(data)
    else:
        raise ValueError("Data must be a list of dictionaries.")

    df.to_csv(file_name, index=False)
    print(f"Data exported to {file_name} successfully.")
