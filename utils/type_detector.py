import pandas as pd

def detect_column_types(df):
    """
    Analyzes a Pandas DataFrame and categorizes each column into a data type.
    Categories: 'numeric', 'date', 'text'
    """
    type_mapping = {}
    
    for col in df.columns:
        # 1. Check if the column is purely numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            type_mapping[col] = 'numeric'
            continue
        
        # 2. Check if it's a date
        sample = df[col].dropna() # Ignore empty rows for the test
        if len(sample) > 0:
            try:
                # If Pandas can convert it to a datetime object, it's a date
                pd.to_datetime(sample, format='mixed', errors='raise')
                type_mapping[col] = 'date'
                continue
            except (ValueError, TypeError):
                pass # If it crashes, it's not a date, move to the next check
        
        # 3. If it's not a number and not a date, we treat it as text
        type_mapping[col] = 'text'
        
    return type_mapping

# --- TESTING BLOCK ---
# This block ONLY runs if we execute this specific file. 
if __name__ == "__main__":
    # Load our messy dataset
    test_df = pd.read_csv('sample_data/sample_messy.csv')
    
    print("--- Testing Type Detector ---")
    
    # Run our function
    detected_types = detect_column_types(test_df)
    
    # Print the results nicely
    for column_name, data_type in detected_types.items():
        print(f"{column_name}: {data_type}")
        