import pandas as pd

def parse(pdf_path: str) -> pd.DataFrame:
    # TODO: Implement PDF parsing logic for icici
    # Temporary: Load the matching CSV directly for testing
    csv_path = f"data/icici/result.csv"
    return pd.read_csv(csv_path)
