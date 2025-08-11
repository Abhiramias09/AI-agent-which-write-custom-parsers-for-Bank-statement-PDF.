import os
import sys
import argparse
import importlib
import pandas as pd
import pdfplumber
from pathlib import Path

# ---------- SETTINGS ----------
ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
PARSER_DIR = ROOT_DIR / "custom_parsers"
MAX_ATTEMPTS = 3

# ---------- PARSER TEMPLATE ----------
PARSER_TEMPLATE = """
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
                        parts = re.split(r"\\s{2,}", line.strip())
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
"""

# ---------- FUNCTIONS ----------
def write_parser_file(bank: str, code: str):
    PARSER_DIR.mkdir(exist_ok=True)
    parser_path = PARSER_DIR / f"{bank}_parser.py"
    with open(parser_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Parser file created at {parser_path}")

def run_parser(bank: str, pdf_path: Path):
    sys.path.insert(0, str(PARSER_DIR))
    parser_module = importlib.import_module(f"{bank}_parser")
    return parser_module.parse(str(pdf_path))

def compare_with_csv(df_parsed: pd.DataFrame, csv_path: Path):
    df_expected = pd.read_csv(csv_path, dtype=str).fillna("")
    df_parsed = df_parsed.fillna("").astype(str)

    print("\nExpected columns:", df_expected.columns.tolist())
    print("Parsed columns:", df_parsed.columns.tolist())
    print("\nFirst few expected rows:\n", df_expected.head())
    print("\nFirst few parsed rows:\n", df_parsed.head())

    return df_expected.equals(df_parsed)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Bank name (e.g., icici, sbi)")
    args = parser.parse_args()
    bank = args.target.lower()

    # ✅ Directly point ICICI to your desktop path
    if bank == "icici":
        csv_path = Path(r"C:\Users\abhir\Desktop\AI Agent\ai-agent-challenge\data\icici\result.csv")
        pdf_path = DATA_DIR / bank / f"{bank} sample.pdf"
    else:
        pdf_path = DATA_DIR / bank / f"{bank} sample.pdf"
        csv_path = DATA_DIR / bank / "result.csv"

    if not pdf_path.exists() or not csv_path.exists():
        print(f"❌ Missing PDF or CSV for {bank}")
        print(f"Looking for PDF at: {pdf_path}")
        print(f"Looking for CSV at: {csv_path}")
        return

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n--- Attempt {attempt} ---")
        write_parser_file(bank, PARSER_TEMPLATE)

        try:
            df_parsed = run_parser(bank, pdf_path)
        except Exception as e:
            print(f"❌ Error running parser: {e}")
            continue

        if compare_with_csv(df_parsed, csv_path):
            print("✅ Success! Parser output matches CSV.")
            return
        else:
            print("❌ Output does not match CSV. Retrying...")

    print("\n❌ Failed to create a working parser after multiple attempts.")

if __name__ == "__main__":
    main()
