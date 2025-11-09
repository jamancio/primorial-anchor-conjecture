# ==============================================================================
# PRIMORIAL ANCHOR CONJECTURE (PAC) - TEST 3: Residue Class Analysis (Mod 30)
#
# This test analyzes the distribution of composite k failures based on the
# residue class of the S_n anchor modulo 30 (P_3).
#
# GOAL:
# 1. Confirm the PAC prediction for S_n % 30 == 0 (no k % 3 or k % 5).
# 2. Explore if different non-zero residue classes (S_n % 30 != 0)
#    exhibit distinct patterns in the types of composite k failures
#    they produce.
# ==============================================================================

import math
import time
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt"
MAX_PRIME_PAIRS_TO_TEST = 50000000
START_INDEX = 10 # Consistent start to avoid small prime anomalies

# --- Function to load primes from a file ---
def load_primes_from_file(filename):
    """Loads ALL primes from the text file."""
    print(f"Loading ALL primes from {filename}...")
    start_time = time.time()
    try:
        with open(filename, 'r') as f:
            prime_list = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        return None, None
    
    prime_set = set(prime_list)
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes and created set in {end_time - start_time:.2f} seconds.")
    
    required_primes = MAX_PRIME_PAIRS_TO_TEST + START_INDEX + 10
    if len(prime_list) < required_primes:
        print(f"\nFATAL ERROR: Prime file is too small.")
        return None, None
        
    return prime_list, prime_set

# --- Main Testing Logic ---
def run_PAC_residue_analysis_mod30():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PAC Residue Class Analysis (Mod 30) for {MAX_PRIME_PAIRS_TO_TEST:,} S_n pairs...")
    print(f"  - Analyzing distribution of k failures for each S_n % 30 residue class.")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for the test ---
    total_law_I_failures = 0
    
    # Dictionary to hold failure data: {residue: {k_composite: count}}
    failures_by_residue = {i: defaultdict(int) for i in range(30)}
    
    loop_end_index = MAX_PRIME_PAIRS_TO_TEST + START_INDEX
    
    for i in range(START_INDEX, loop_end_index):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - START_INDEX + 1
            print(f"Progress: {progress:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_S_n = p_n + p_n_plus_1

        # --- 1. Find the Law I Failure ---
        min_distance_k = 0
        q_prime = 0
        search_dist = 1
        
        while True:
            q_lower = anchor_S_n - search_dist
            q_upper = anchor_S_n + search_dist

            if q_lower in prime_set:
                min_distance_k = search_dist
                q_prime = q_lower
                break
            if q_upper in prime_set:
                min_distance_k = search_dist
                q_prime = q_upper
                break
                
            search_dist += 1
            if search_dist > 2000: break 
        
        if min_distance_k == 0: continue 

        # --- 2. Check if it's a composite failure ---
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            total_law_I_failures += 1
            
            # --- 3. Classify by Residue (Mod 30) ---
            residue_mod_30 = anchor_S_n % 30
            
            # Record the specific composite k for this residue
            failures_by_residue[residue_mod_30][min_distance_k] += 1
            
    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " PAC-3: RESIDUE CLASS ANALYSIS (MOD 30) REPORT " + "="*20)
    print(f"\nTotal S_n Anchors Analyzed: {MAX_PRIME_PAIRS_TO_TEST:,}")
    print(f"Total Law I Failures (Composite k) Found: {total_law_I_failures:,}")

    # --- Analyze each residue class ---
    print("\n--- Analysis by S_n % 30 Residue Class ---")
    
    phi_30 = 8 # Number of residues coprime to 30
    possible_S_n_residues = []
    # S_n = p_n + p_{n+1}. If p_n, p_{n+1} > 5, then p_n, p_{n+1} are coprime to 30.
    # The possible residues for primes > 5 mod 30 are {1, 7, 11, 13, 17, 19, 23, 29}.
    # S_n can only be the sum of two such residues (mod 30).
    prime_residues = {1, 7, 11, 13, 17, 19, 23, 29}
    for r1 in prime_residues:
        for r2 in prime_residues:
            possible_S_n_residues.append((r1 + r2) % 30)
    possible_S_n_residues = sorted(list(set(possible_S_n_residues)))
    print(f"\nExpected non-zero S_n % 30 residues (for n>3): {possible_S_n_residues}")
    print("(Note: Includes residue 0, e.g., 1+29=30, 7+23=30, 13+17=30)")


    for residue in range(30):
        failure_data = failures_by_residue[residue]
        total_failures_in_class = sum(failure_data.values())
        
        print("\n" + "-" * 20 + f" S_n % 30 == {residue} " + "-" * 20)
        print(f"  Total Failures in this Class: {total_failures_in_class:,}")
        
        if not failure_data:
            if residue not in possible_S_n_residues and residue != 0: # Check if residue is expected
                 print("  (This residue class is not expected for S_n where n > 3)")
            continue

        # Check PAC prediction for residue 0
        if residue == 0:
            forbidden_k_found = {k for k in failure_data if k % 3 == 0 or k % 5 == 0}
            if not forbidden_k_found:
                print("  [PAC VERIFIED] No k divisible by 3 or 5 found.")
            else:
                print(f"  [PAC FALSIFIED?] Found k divisible by 3 or 5: {forbidden_k_found}")

        # Show top 5 most frequent k values for this class
        print("  Top 5 Composite k Values:")
        sorted_k = sorted(failure_data.items(), key=lambda item: item[1], reverse=True)
        for k, count in sorted_k[:5]:
             percentage = (count / total_failures_in_class) * 100 if total_failures_in_class else 0
             print(f"    - k = {k:<5}: {count:<10,} ({percentage:.2f}%)")
        if len(sorted_k) > 5:
            print("    ...")

    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    print("\n  Analysis complete. Review the distributions above.")
    print("  Key points to check:")
    print("  1. Does the S_n % 30 == 0 class confirm the PAC prediction?")
    print("  2. Do other residue classes show significantly different")
    print("     distributions of common k failures (e.g., 9, 15, 25)?")

    print("=" * (50 + len(" FINAL CONCLUSION ")))

if __name__ == "__main__":
    run_PAC_residue_analysis_mod30()