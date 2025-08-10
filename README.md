# AI PDF Parser Agent

This project implements an AI agent that can automatically generate custom parsers for PDF bank statements. The agent follows a loop of **plan → generate code → run tests → self-fix** (up to 3 attempts) and produces a parser that outputs data matching the expected CSV format.

---

🛠 Features
- Command-line interface to target a specific bank.
- Automatically generates a parser file in `custom_parsers/` if missing.
- Validates parser output against expected CSV using `pandas.DataFrame.equals`.
- Supports multiple banks (e.g., ICICI, SBI, etc.).
- Modular parser contract: `parse(pdf_path) -> pd.DataFrame`.

---

🚀 How to Run

### **1. Clone the repository**
```bash
git clone <repo-url>
cd ai-agent-challenge

2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Place your data
PDF: data/<bank>/<bank>_sample.pdf

Expected CSV: data/<bank>/result.csv

4. Run the agent
bash
Copy
Edit
python agent.py --target icici
This will read the PDF & CSV.

If the parser doesn’t exist, it will generate custom_parsers/icici_parser.py.

5. Check the result
If the output matches the CSV:

kotlin
Copy
Edit
🎉 Test passed! Parsed data matches expected CSV.
Otherwise, the agent will attempt to fix the parser (max 3 retries).

📊 Agent Workflow Diagram
pgsql
Copy
Edit
+----------------+
| Start CLI Call |
+-------+--------+
        |
        v
+-------+--------+
| Load Target    |
| Bank Data      |
+-------+--------+
        |
        v
+-------+--------+
| Parser Exists? |
+---+-------+----+
    | Yes    | No
    v        v
 Run Test  Generate Parser
            |
            v
        Run Test
            |
            v
   +--------+--------+
   | Matches Expected?|
   +---+----------+---+
       | Yes      | No
       v          v
   Print ✅    Retry ≤ 3
                |
                v
         Print ❌ if fail
