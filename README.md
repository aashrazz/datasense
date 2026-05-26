# 📊 DataSense: Automated Data Quality Analyzer

**Live Demo:** [Insert your live Streamlit URL here]

DataSense is a full-stack, cloud-hosted data engineering tool that acts as an automated health inspector for datasets. By uploading any CSV file, the engine instantly evaluates the data across five critical dimensions, assigns a comprehensive quality score out of 100, and generates a downloadable PDF scorecard.

This tool is designed to catch missing values, formatting inconsistencies, duplicates, and logical errors before the data is used for machine learning or business intelligence.

## ⚙️ The 5 Dimensions of Data Quality
The backend engine uses custom Pandas and NumPy logic to evaluate the following:

1. **Completeness (20 pts):** Scans the entire dataset for missing, null, or empty values (`NaN`, `" "`, `"N/A"`).
2. **Consistency (20 pts):** Identifies mixed text casing (e.g., `Mumbai` vs `mumbai`), mixed date formats (`-` vs `/`), and inconsistent string lengths.
3. **Uniqueness (20 pts):** Flags full-row duplicates and column-specific duplicates for identifiers like IDs, emails, and phone numbers.
4. **Validity (20 pts):** Uses regular expressions to catch broken email formats and identifies impossible numeric values (e.g., negative prices or negative horsepower).
5. **Accuracy (20 pts):** Performs cross-field logical checks (e.g., ensuring a `last_purchase_date` does not chronologically precede a `signup_date`).

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python-native UI)
* **Backend Data Engine:** Pandas, NumPy
* **Report Generation:** ReportLab (PDF export)
* **Deployment:** Streamlit Community Cloud

## 📂 Project Structure
```text
datasense/
│
├── analyzer/                 # Core data engineering logic
│   ├── __init__.py
│   ├── scorer.py             # Master script that aggregates all 5 dimensions
│   ├── completeness.py
│   ├── consistency.py
│   ├── uniqueness.py
│   ├── validity.py
│   └── accuracy.py
│
├── utils/                    # Helper functions
│   ├── pdf_generator.py      # ReportLab PDF creation logic
│   └── type_detector.py      # Auto-detects numeric/date/string columns
│
├── sample_data/
│   └── sample_messy.csv      # Test dataset
│
├── app.py                    # Streamlit frontend and UI layout
├── requirements.txt          # Deployment dependencies
└── README.md
