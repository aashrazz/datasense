import pandas as pd

# Import our 5 custom-built dimensions
from analyzer.completeness import evaluate_completeness
from analyzer.consistency import evaluate_consistency
from analyzer.uniqueness import evaluate_uniqueness
from analyzer.validity import evaluate_validity
from analyzer.accuracy import evaluate_accuracy

def generate_scorecard(df):
    """
    Runs the dataset through all 5 dimensions, aggregates the scores, 
    and calculates a final grade based on the project brief.
    """
    # 1. Run all 5 checks
    comp_results = evaluate_completeness(df)
    cons_results = evaluate_consistency(df)
    uniq_results = evaluate_uniqueness(df)
    val_results = evaluate_validity(df)
    acc_results = evaluate_accuracy(df)

    # 2. Calculate Total Score (out of 100)
    total_score = (
        comp_results['score'] +
        cons_results['score'] +
        uniq_results['score'] +
        val_results['score'] +
        acc_results['score']
    )
    total_score = round(total_score, 1)

    # 3. Determine Grade Bands
    if total_score >= 90:
        grade = "Excellent"
        verdict = "Data is production-ready."
    elif total_score >= 75:
        grade = "Good"
        verdict = "Minor issues, fix before use."
    elif total_score >= 60:
        grade = "Fair"
        verdict = "Significant issues, clean before analysis."
    elif total_score >= 40:
        grade = "Poor"
        verdict = "Major structural problems."
    else:
        grade = "Critical"
        verdict = "Data needs a complete overhaul."

    # 4. Package everything up cleanly to send to the web app
    return {
        "total_score": total_score,
        "grade": grade,
        "verdict": verdict,
        "dimensions": {
            "Completeness": comp_results,
            "Consistency": cons_results,
            "Uniqueness": uniq_results,
            "Validity": val_results,
            "Accuracy": acc_results
        }
    }

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_df = pd.read_csv('sample_data/sample_messy.csv')
    
    print("--- Generating Master Scorecard ---")
    final_report = generate_scorecard(test_df)
    
    print(f"\nFINAL SCORE: {final_report['total_score']} / 100")
    print(f"GRADE: [{final_report['grade']}] - {final_report['verdict']}\n")
    
    print("--- Dimension Breakdown ---")
    for dim_name, data in final_report['dimensions'].items():
        print(f"{dim_name}: {data['score']} / 20.0")

        