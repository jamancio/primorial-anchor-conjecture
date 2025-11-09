# ==============================================================================
# PAC-LAW III CORRELATION ANALYSIS SCRIPT
#
# Reads the CSV output from 'run_PAC_Law3_correlation_test()' and performs
# statistical analysis to look for correlations.
#
# Requires the 'pandas' library: pip install pandas
# ==============================================================================

import pandas as pd
from collections import Counter
import time

# --- Configuration ---
INPUT_CSV_FILE = "pac_law3_correlation_data.csv"

# --- Main Analysis Logic ---
def analyze_correlation_data():
    print(f"Loading correlation data from {INPUT_CSV_FILE}...")
    start_time = time.time()
    try:
        # Load the entire CSV into a pandas DataFrame
        df = pd.read_csv(INPUT_CSV_FILE)
    except FileNotFoundError:
        print(f"FATAL ERROR: The file '{INPUT_CSV_FILE}' was not found.")
        print("Please run the 'run_PAC_Law3_correlation_test()' script first.")
        return
    except Exception as e:
        print(f"FATAL ERROR: Could not load or parse the CSV file: {e}")
        return

    load_time = time.time() - start_time
    print(f"Loaded {len(df):,} failure records in {load_time:.2f} seconds.")
    print("-" * 80)

    if df.empty:
        print("The CSV file is empty. No Law I failures were recorded.")
        return

    # --- Basic Sanity Checks ---
    total_failures = len(df)
    max_r_observed = df['fix_radius_r'].max()
    print(f"Basic Stats:")
    print(f"  Total Law I Failures Analyzed: {total_failures:,}")
    print(f"  Maximum Law III Radius (r_max) Observed: {max_r_observed}")
    print("-" * 80)

    # --- Analysis 1: Distribution of Fixing Radius 'r' ---
    print("\n--- Distribution of Fixing Radius (r) ---")
    radius_counts = df['fix_radius_r'].value_counts().sort_index()
    cumulative_count = 0
    print(f"{'Radius (r)':<12} | {'Count':<15} | {'Percentage':<12} | {'Cumulative %':<15}")
    print("-" * 60)
    for r, count in radius_counts.items():
        percentage = (count / total_failures) * 100
        cumulative_count += count
        cumulative_percentage = (cumulative_count / total_failures) * 100
        print(f"{r:<12} | {count:<15,} | {percentage:<12.2f}% | {cumulative_percentage:<15.2f}%")
    print("-" * 60)
    print(f"{'TOTAL':<12} | {total_failures:<15,} | {100.0:<12.2f}% | {100.0:<15.2f}%")
    print("-" * 80)

    # --- Analysis 2: Average 'r' by S_n Modulo Signature ---
    # We focus on Mod 30 as it showed distinct patterns in Test 3
    print("\n--- Average Fixing Radius (r) by S_n % 30 Residue Class ---")
    # Calculate the mean 'r' for each Sn_mod30 group
    avg_r_by_sn_mod30 = df.groupby('Sn_mod30')['fix_radius_r'].mean().sort_index()
    # Calculate the count of failures for each Sn_mod30 group
    count_by_sn_mod30 = df['Sn_mod30'].value_counts().sort_index()

    print(f"{'S_n % 30':<10} | {'Failure Count':<15} | {'Average Fix Radius (r)':<25}")
    print("-" * 55)
    # Get all possible residues that actually appeared in the data
    present_residues = count_by_sn_mod30.index
    for residue in sorted(present_residues):
        avg_r = avg_r_by_sn_mod30.get(residue, float('nan')) # Use .get for safety
        count = count_by_sn_mod30.get(residue, 0)
        if count > 0: # Only print residues that had failures
             print(f"{residue:<10} | {count:<15,} | {avg_r:<25.4f}")
    print("-" * 55)
    print("Interpretation: Does the average 'r' vary significantly between classes?")
    print("              Are 'perfect' anchors (residue 0) fixed faster on average?")
    print("-" * 80)

    # --- Analysis 3: S_fix Signature Distribution for S_n % 30 == 0 ---
    print("\n--- Fixing Anchor (S_fix % 30) Distribution for S_n % 30 == 0 Failures ---")
    # Filter data for only the "perfect" S_n anchors
    perfect_sn_failures = df[df['Sn_mod30'] == 0]
    if not perfect_sn_failures.empty:
        sfix_counts = perfect_sn_failures['Sfix_mod30'].value_counts().sort_index()
        total_perfect_failures = len(perfect_sn_failures)

        print(f"Total Failures from S_n % 30 == 0: {total_perfect_failures:,}")
        print(f"{'S_fix % 30':<12} | {'Count':<15} | {'Percentage':<12}")
        print("-" * 45)
        for residue, count in sfix_counts.items():
            percentage = (count / total_perfect_failures) * 100
            print(f"{residue:<12} | {count:<15,} | {percentage:<12.2f}%")
        print("-" * 45)
        print("Interpretation: When a perfect anchor fails (rarely),")
        print("              do the fixing anchors tend to fall into specific classes?")
    else:
        print("No failures were recorded for S_n % 30 == 0.")
    print("-" * 80)

    # --- Analysis 4: S_fix Signature Distribution for a specific high-failure class ---
    # Example: Analyze S_n % 30 == 12 (which was prone to k=25 in Test 3)
    target_residue = 12
    print(f"\n--- Fixing Anchor (S_fix % 30) Distribution for S_n % 30 == {target_residue} Failures ---")
    specific_sn_failures = df[df['Sn_mod30'] == target_residue]
    if not specific_sn_failures.empty:
        sfix_counts_specific = specific_sn_failures['Sfix_mod30'].value_counts().sort_index()
        total_specific_failures = len(specific_sn_failures)

        print(f"Total Failures from S_n % 30 == {target_residue}: {total_specific_failures:,}")
        print(f"{'S_fix % 30':<12} | {'Count':<15} | {'Percentage':<12}")
        print("-" * 45)
        for residue, count in sfix_counts_specific.items():
            percentage = (count / total_specific_failures) * 100
            print(f"{residue:<12} | {count:<15,} | {percentage:<12.2f}%")
        print("-" * 45)
        print(f"Interpretation: When an S_n % 30 == {target_residue} anchor fails,")
        print("               do the fixing anchors avoid certain classes or prefer others?")
    else:
        print(f"No failures were recorded for S_n % 30 == {target_residue}.")
    print("-" * 80)


    print("\nAnalysis complete. Further statistical tests (e.g., correlations,")
    print("chi-squared tests) can be applied to this DataFrame for deeper insights.")

if __name__ == "__main__":
    analyze_correlation_data()