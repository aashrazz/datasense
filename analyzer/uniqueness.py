import pandas as pd

def evaluate_uniqueness(df):
    """
    Checks for exact duplicate rows and duplicate values in columns that should be unique.
    Returns a score out of 20.
    """
    total_rows = len(df)
    if total_rows == 0:
        return {"score": 0.0, "issues": pd.DataFrame()}

    issues = []
    
    # 1. Check for exact duplicate rows across the entire dataset
    duplicate_rows = df[df.duplicated(keep=False)]
    num_duplicate_rows = len(duplicate_rows)
    
    if num_duplicate_rows > 0:
        issues.append({
            'Type': 'Full Row Duplicates',
            'Column/Scope': 'Entire Dataset',
            'Duplicate_Count': num_duplicate_rows,
            'Examples': f"Rows: {', '.join(duplicate_rows.index[:5].astype(str).tolist())}"
        })

    # 2. Check for duplicate values in columns that usually require uniqueness
    # We look for keywords in the column names
    unique_keywords = ['id', 'email', 'phone', 'code', 'number']
    
    for col in df.columns:
        # Check if the column name contains any of our target keywords
        if any(keyword in col.lower() for keyword in unique_keywords):
            # Ignore missing values for this check
            clean_col = df[col].dropna()
            
            # Find values that appear more than once
            duplicates = clean_col[clean_col.duplicated(keep=False)]
            num_duplicates = len(duplicates)
            
            if num_duplicates > 0:
                # Grab a few examples of the duplicated values
                example_vals = ", ".join(duplicates.unique()[:3].astype(str))
                issues.append({
                    'Type': 'Column Duplicates',
                    'Column/Scope': col,
                    'Duplicate_Count': num_duplicates,
                    'Examples': f"Values: {example_vals}"
                })

    # 3. Calculate Score (Max 20 points)
    # Brief rules: 0 duplicates = 20 pts. >10% duplicates = 0 pts. Linear scale.
    total_duplicate_flags = sum(issue['Duplicate_Count'] for issue in issues)
    duplicate_percentage = (total_duplicate_flags / total_rows) * 100

    if duplicate_percentage == 0:
        score = 20
    elif duplicate_percentage >= 10:
        score = 0
    else:
        # Scale: 5% duplicates = 10 points
        score = 20 - (duplicate_percentage * 2)

    if issues:
        issues_df = pd.DataFrame(issues)
    else:
        issues_df = pd.DataFrame(columns=['Type', 'Column/Scope', 'Duplicate_Count', 'Examples'])

    return {
        "score": round(max(0, score), 1),
        "issues": issues_df
    }

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_df = pd.read_csv('sample_data/sample_messy.csv')
    
    print("--- Testing Dimension 3: Uniqueness ---")
    results = evaluate_uniqueness(test_df)
    
    print(f"Final Score: {results['score']} / 20.0\n")
    print("Issues Found:")
    if not results['issues'].empty:
        print(results['issues'].to_string(index=False))
    else:
        print("No uniqueness issues found!")
        