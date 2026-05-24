import pandas as pd
import numpy as np

def evaluate_completeness(df):
    """
    Checks the dataset for missing values (nulls, blanks, 'NA', etc.).
    Returns a score out of 20 and a detailed breakdown of missing data per column.
    """
    # 1. Define what a "missing" value looks like
    missing_indicators = ["", " ", "NA", "N/A", "none", "null", "NaN"]
    
    # Create a copy so we don't mess up the original data, and replace text nulls with actual computer nulls (np.nan)
    # We use a dictionary with regex=False to safely replace these exact strings
    df_clean = df.replace(missing_indicators, np.nan)
    
    # 2. Calculate the math
    total_rows = len(df_clean)
    total_cells = df_clean.size
    
    # Count missing values per column
    missing_counts = df_clean.isna().sum()
    missing_percentages = (missing_counts / total_rows) * 100
    
    total_missing = missing_counts.sum()
    completeness_pct = ((total_cells - total_missing) / total_cells) * 100
    
    # 3. Calculate the Score (Max 20 points)
    # Brief rules: 100% complete = 20 pts. Below 80% = 0 pts.
    if completeness_pct == 100:
        score = 20
    elif completeness_pct <= 80:
        score = 0
    else:
        # Linear scale: 90% complete equals 10 points. 95% equals 15 points.
        score = completeness_pct - 80 

    # 4. Create a clean table to show the user exactly what is missing
    details = pd.DataFrame({
        'Column': missing_counts.index,
        'Missing_Count': missing_counts.values,
        'Missing_Percentage': missing_percentages.values.round(2)
    })
    
    # Filter the table to only show columns that actually have missing data
    issues_only = details[details['Missing_Count'] > 0].reset_index(drop=True)

    return {
        "score": round(score, 1),
        "overall_completeness": round(completeness_pct, 1),
        "issues": issues_only
    }

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_df = pd.read_csv('sample_data/sample_messy.csv')
    
    print("--- Testing Dimension 1: Completeness ---")
    results = evaluate_completeness(test_df)
    
    print(f"Final Score: {results['score']} / 20.0")
    print(f"Overall Completeness: {results['overall_completeness']}%\n")
    print("Issues Found:")
    print(results['issues'])
    