import pandas as pd
from dateutil import parser

def evaluate_accuracy(df):
    """
    Checks for logical inconsistencies between different columns.
    e.g., Does end_date happen BEFORE start_date?
    Returns a score out of 20.
    """
    issues = []
    
    # 1. Date Logic Check: Signup Date vs Last Purchase Date
    # A user cannot make a purchase BEFORE they sign up.
    if 'signup_date' in df.columns and 'last_purchase_date' in df.columns:
        # We need to temporarily convert these text columns into actual computer dates to do math on them
        # coerce means if a date is totally broken, just turn it into a NaT (Not a Time) so it doesn't crash the program
        temp_signup = pd.to_datetime(df['signup_date'], format='mixed', errors='coerce')
        temp_purchase = pd.to_datetime(df['last_purchase_date'], format='mixed', errors='coerce')
        
        # Find rows where the purchase happened before signup
        invalid_dates = df[temp_purchase < temp_signup]
        
        if len(invalid_dates) > 0:
            issues.append({
                'Logic_Rule': 'Purchase date cannot be before signup date',
                'Rows_Affected': len(invalid_dates),
                'Examples': f"Rows: {', '.join(invalid_dates.index[:3].astype(str).tolist())}"
            })

    # Calculate Score (Max 20 points)
    # Deduct 5 points for every logical rule that fails
    deduction = len(issues) * 5
    score = max(0, 20 - deduction)

    if issues:
        issues_df = pd.DataFrame(issues)
    else:
        issues_df = pd.DataFrame(columns=['Logic_Rule', 'Rows_Affected', 'Examples'])

    return {
        "score": float(score),
        "issues": issues_df
    }

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_df = pd.read_csv('sample_data/sample_messy.csv')
    
    print("--- Testing Dimension 5: Accuracy ---")
    results = evaluate_accuracy(test_df)
    
    print(f"Final Score: {results['score']} / 20.0\n")
    print("Issues Found:")
    if not results['issues'].empty:
        print(results['issues'].to_string(index=False))
    else:
        print("No accuracy issues found!")
        