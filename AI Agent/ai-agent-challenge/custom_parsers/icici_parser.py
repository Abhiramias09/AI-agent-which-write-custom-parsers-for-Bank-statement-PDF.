
import pandas as pd
import pdfplumber
import re

def parse(pdf_path: str) -> pd.DataFrame:
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        if row and any(cell for cell in row):
                            rows.append([cell.strip() if cell else "" for cell in row])
            else:
                text = page.extract_text() or ""
                for line in text.splitlines():
                    if any(char.isdigit() for char in line):
                        parts = re.split(r"\s{2,}", line.strip())
                        rows.append(parts)

    df = pd.DataFrame(rows)

    if df.shape[1] == 5:
        df.columns = ["Date", "Description", "Withdrawal", "Deposit", "Balance"]
    else:
        df.columns = [f"col{i}" for i in range(df.shape[1])]

    # 🔹 Map to expected column names
    col_map = {
        "Withdrawal": "Debit Amt",
        "Deposit": "Credit Amt"
    }
    df.rename(columns=col_map, inplace=True)

    # 🔹 Remove duplicate header rows
    if "Date" in df.columns:
        df = df[df["Date"] != "Date"]

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df.reset_index(drop=True, inplace=True)
    return df
