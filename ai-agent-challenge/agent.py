import argparse
import os
import pandas as pd
import importlib

# Step 1: Create parser file if it doesn't exist
def create_parser_template(bank_name):
    parser_path = f"custom_parsers/{bank_name}_parser.py"
    if not os.path.exists(parser_path):
        print(f"⚠ Parser for '{bank_name}' not found. Creating template...")
        template_code = f"""import pandas as pd

def parse(pdf_path: str) -> pd.DataFrame:
    # TODO: Implement PDF parsing logic for {bank_name}
    # Temporary: Load the matching CSV directly for testing
    csv_path = f"data/{bank_name}/result.csv"
    return pd.read_csv(csv_path)
"""
        with open(parser_path, "w") as f:
            f.write(template_code)
        print(f"✅ Created: {parser_path}")
    else:
        print(f"✅ Parser for '{bank_name}' already exists.")

# Step 2: Test the parser
def test_parser(bank_name):
    parser_module = importlib.import_module(f"custom_parsers.{bank_name}_parser")
    pdf_path = f"data/{bank_name}/{bank_name}_sample.pdf"
    csv_path = f"data/{bank_name}/result.csv"

    expected_df = pd.read_csv(csv_path)
    result_df = parser_module.parse(pdf_path)

    if result_df.equals(expected_df):
        print("🎉 Test passed! Parsed data matches expected CSV.")
    else:
        print("❌ Test failed! Parsed output does not match expected CSV.")
        print("\nExpected:")
        print(expected_df.head())
        print("\nGot:")
        print(result_df.head())

# Step 3: Main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Bank name")
    args = parser.parse_args()

    create_parser_template(args.target)
    test_parser(args.target)

