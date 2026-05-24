import pandas as pd

def evaluate_consistency(df):
    """
    Checks for formatting consistency in columns (mixed casing, mixed date formats, mixed lengths).
    Returns a score out of 20.
    """
    issues = []
    
    for col in df.columns:
        # Drop empty rows just for this check (we already scored them in completeness)
        clean_col = df[col].dropna().astype(str)
        if len(clean_col) == 0:
            continue
            
        # 1. Check for mixed text casing
        # If lowercasing everything shrinks the list of unique values, we have a mix (e.g. Mumbai vs mumbai)
        if clean_col.str.lower().nunique() < clean_col.nunique():
            issues.append({
                'Column': col,
                'Issue': 'Mixed text casing',
                'Example_Values': ", ".join(clean_col.unique()[:3])
            })
            
        # 2. Check for mixed date formats
        # We look for columns that have BOTH hyphens (-) and slashes (/) 
        if clean_col.str.contains(r'\d').any(): # Has numbers
            has_slashes = clean_col.str.contains('/').any()
            has_dashes = clean_col.str.contains('-').any()
            if has_slashes and has_dashes:
                issues.append({
                    'Column': col,
                    'Issue': 'Mixed date formats (- and /)',
                    'Example_Values': ", ".join(clean_col.unique()[:3])
                })
                
        # 3. Check for mixed phone number/ID lengths
        if 'phone' in col.lower() or 'id' in col.lower():
            lengths = clean_col.str.len().unique()
            if len(lengths) > 1:
                issues.append({
                    'Column': col,
                    'Issue': f'Mixed character lengths: {lengths}',
                    'Example_Values': ", ".join(clean_col.unique()[:3])
                })

    # Scoring: Start with 20. Deduct 4 points for every inconsistent column found.
    deduction = len(issues) * 4
    score = max(0, 20 - deduction) # Score can't go below 0
    
    # Format the output table safely
    if issues:
        issues_df = pd.DataFrame(issues)
    else:
        issues_df = pd.DataFrame(columns=['Column', 'Issue', 'Example_Values'])

    return {
        "score": float(score),
        "issues": issues_df
    }

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_df = pd.read_csv('sample_data/sample_messy.csv')
    
    print("--- Testing Dimension 2: Consistency ---")
    results = evaluate_consistency(test_df)
    
    print(f"Final Score: {results['score']} / 20.0\n")
    print("Issues Found:")
    if not results['issues'].empty:
        print(results['issues'].to_string(index=False))
    else:
        print("No consistency issues found!")
        