import pandas as pd
import numpy as np
import re

def evaluate_validity(df):
    """
    Checks if values fall within expected ranges and formats.
    (Emails have @, dates are real, numbers aren't extreme outliers).
    Returns a score out of 20.
    """
    issues = []
    
    for col in df.columns:
        clean_col = df[col].dropna()
        if len(clean_col) == 0:
            continue

        # 1. Check Emails using a Regex (Regular Expression) pattern
        if 'email' in col.lower():
            # This pattern means: "text" + "@" + "text" + "." + "text"
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            
            # Find emails that DO NOT match the pattern
            invalid_emails = clean_col[~clean_col.astype(str).str.match(email_regex)]
            
            if len(invalid_emails) > 0:
                issues.append({
                    'Column': col,
                    'Issue': 'Invalid Email Format (Missing @ or domain)',
                    'Invalid_Count': len(invalid_emails),
                    'Examples': ", ".join(invalid_emails.astype(str).unique()[:3])
                })

        # 2. Check Numeric Outliers using IQR (Interquartile Range)
        # We ignore IDs and Pincodes because they are numbers, but we don't calculate outliers for them
        elif pd.api.types.is_numeric_dtype(df[col]) and 'id' not in col.lower() and 'pincode' not in col.lower():
            Q1 = clean_col.quantile(0.25)
            Q3 = clean_col.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find numbers outside the normal range
            outliers = clean_col[(clean_col < lower_bound) | (clean_col > upper_bound)]
            if len(outliers) > 0:
                issues.append({
                    'Column': col,
                    'Issue': 'Numeric Outliers Detected',
                    'Invalid_Count': len(outliers),
                    'Examples': ", ".join(outliers.astype(str).unique()[:3])
                })

    # Calculate Score (Max 20)
    # Deduct 5 points for every column that has validity issues
    deduction = len(issues) * 5
    score = max(0, 20 - deduction)

    if issues:
        issues_df = pd.DataFrame(issues)
    else:
        issues_df = pd.DataFrame(columns=['Column', 'Issue', 'Invalid_Count', 'Examples'])

    return {
        "score": float(score),
        "issues": issues_df
    }

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_df = pd.read_csv('sample_data/sample_messy.csv')
    
    print("--- Testing Dimension 4: Validity ---")
    results = evaluate_validity(test_df)
    
    print(f"Final Score: {results['score']} / 20.0\n")
    print("Issues Found:")
    if not results['issues'].empty:
        print(results['issues'].to_string(index=False))
    else:
        print("No validity issues found!")
        