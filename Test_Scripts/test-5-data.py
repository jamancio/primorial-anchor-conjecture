# ==============================================================================
# PRIMORIAL ANCHOR CONJECTURE (PAC) - TEST 5: PAC-Law III Correlation Test
#
# This test investigates the direct link between the PAC's primorial
# classification and the observed efficiency (small r_max) of PAS Law III.
#
# METHODOLOGY:
# 1. Use the S_n = p_n + p_{n+1} sequence.
# 2. Find all "Law I Failures" (composite 'k_min').
# 3. For each failure:
#    a. Record the primorial signatures (mod 6, 30, 210) of the failing
#       anchor S_n.
#    b. Simulate the PAS Law III search (r=1, 2, ...) to find the
#       *actual* fixing radius 'r' and the fixing anchor S_fix = S_{n +/- r}.
#    c. Record 'r' and the primorial signatures (mod 6, 30, 210) of S_fix.
# 4. Analyze the collected data for correlations between S_n's signature,
#    the fixing radius 'r', and S_fix's signature.
#
# HYPOTHESIS:
# The efficiency of Law III (small 'r') is correlated with the primorial
# signatures involved, demonstrating PAC as the underlying mechanism.
# ==============================================================================

import math
import time
from collections import defaultdict
import csv # For saving detailed results

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt"
MAX_PRIME_PAIRS_TO_TEST = 50000000
START_INDEX = 10
# Set a reasonable upper limit for the Law III search
MAX_LAW_III_RADIUS = 30
OUTPUT_CSV_FILE = "pac_law3_correlation_data.csv"

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
    
    required_primes = MAX_PRIME_PAIRS_TO_TEST + START_INDEX + MAX_LAW_III_RADIUS + 2
    if len(prime_list) < required_primes:
        print(f"\nFATAL ERROR: Prime file is too small for S_n+r lookups.")
        return None, None
        
    return prime_list, prime_set

def is_clean_k(k_val, prime_set):
    """Helper function to check if k is 1 or a prime."""
    if k_val == 1:
        return True
    # Basic check for small numbers
    if k_val < 2:
        return False
    # Check against the prime set
    return k_val in prime_set

# --- Main Testing Logic ---
def run_PAC_Law3_correlation_test():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PAC-Law III Correlation Test for {MAX_PRIME_PAIRS_TO_TEST:,} S_n pairs...")
    print(f"  - Recording signatures of S_n, S_fix, and fixing radius r.")
    print(f"  - Saving detailed results to {OUTPUT_CSV_FILE}")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for the test ---
    total_law_I_failures = 0
    max_r_observed = 0
    law_III_failures = [] # Should remain empty if Law III holds
    
    # List to store correlation data dictionaries
    correlation_data = []

    # Prepare CSV file
    try:
        csvfile = open(OUTPUT_CSV_FILE, 'w', newline='')
        fieldnames = [
            'n_index', 'Sn', 'q_prime', 'k_composite',
            'Sn_mod6', 'Sn_mod30', 'Sn_mod210',
            'fix_radius_r', 'S_fix',
            'Sfix_mod6', 'Sfix_mod30', 'Sfix_mod210'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    except IOError:
        print(f"FATAL ERROR: Could not open {OUTPUT_CSV_FILE} for writing.")
        return

    # Main loop
    loop_start_index = START_INDEX + MAX_LAW_III_RADIUS # Need buffer for S_{n-r}
    loop_end_index = MAX_PRIME_PAIRS_TO_TEST + loop_start_index
    
    if loop_end_index >= len(prime_list) - MAX_LAW_III_RADIUS -1 :
         print(f"\nFATAL ERROR: Not enough primes loaded for S_n+r lookups at the end.")
         csvfile.close()
         return

    for i in range(loop_start_index, loop_end_index):
        if (i - loop_start_index + 1) % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - loop_start_index + 1
            print(f"Progress: {progress:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Max r: {max_r_observed} | Time: {elapsed:.0f}s", end='\r')

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

            if q_lower > 1 and q_lower in prime_set:
                min_distance_k = search_dist
                q_prime = q_lower
                break
            if q_upper in prime_set:
                min_distance_k = search_dist
                q_prime = q_upper
                break
                
            search_dist += 1
            if search_dist > 3000: break # Increased safety break
        
        if min_distance_k == 0: continue 

        # --- 2. Check if it's a composite failure ---
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            total_law_I_failures += 1
            
            # --- 3. Record S_n Signatures ---
            Sn_mod6 = anchor_S_n % 6
            Sn_mod30 = anchor_S_n % 30
            Sn_mod210 = anchor_S_n % 210
            
            # --- 4. Simulate Law III Search ---
            fix_found = False
            fixing_radius_r = 0
            S_fix = 0
            Sfix_mod6, Sfix_mod30, Sfix_mod210 = -1, -1, -1 # Default invalid values

            for r in range(1, MAX_LAW_III_RADIUS + 1):
                # Check S_{n-r}
                S_prev = prime_list[i - r] + prime_list[i - r + 1]
                k_prev = abs(S_prev - q_prime)
                if is_clean_k(k_prev, prime_set):
                    fix_found = True
                    fixing_radius_r = r
                    S_fix = S_prev
                    break # Fix found

                # Check S_{n+r}
                S_next = prime_list[i + r] + prime_list[i + r + 1]
                k_next = abs(S_next - q_prime)
                if is_clean_k(k_next, prime_set):
                    fix_found = True
                    fixing_radius_r = r
                    S_fix = S_next
                    break # Fix found

            # --- 5. Record Results ---
            if fix_found:
                if fixing_radius_r > max_r_observed:
                    max_r_observed = fixing_radius_r
                
                Sfix_mod6 = S_fix % 6
                Sfix_mod30 = S_fix % 30
                Sfix_mod210 = S_fix % 210

                event_data = {
                    'n_index': i, 'Sn': anchor_S_n, 'q_prime': q_prime, 'k_composite': min_distance_k,
                    'Sn_mod6': Sn_mod6, 'Sn_mod30': Sn_mod30, 'Sn_mod210': Sn_mod210,
                    'fix_radius_r': fixing_radius_r, 'S_fix': S_fix,
                    'Sfix_mod6': Sfix_mod6, 'Sfix_mod30': Sfix_mod30, 'Sfix_mod210': Sfix_mod210
                }
                correlation_data.append(event_data)
                writer.writerow(event_data) # Write to CSV immediately

            else:
                # Law III Failed!
                law_III_failures.append(i)
                print(f"\nFATAL: Law III Falsified at index {i} (S_n={anchor_S_n:,}, q={q_prime:,}, k={min_distance_k:,}). Could not find fix within r={MAX_LAW_III_RADIUS}. Stopping.")
                break # Stop the test immediately

    # Close CSV file
    csvfile.close()

    # --- Final Summary ---
    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Max r: {max_r_observed} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    print("\n" + "="*20 + " PAC-5: PAC-LAW III CORRELATION REPORT " + "="*20)
    print(f"\nTotal S_n Anchors Analyzed: {MAX_PRIME_PAIRS_TO_TEST:,}")
    print(f"Total Law I Failures Found: {total_law_I_failures:,}")
    print(f"Maximum Law III Correction Radius Observed (r_max): {max_r_observed}")
    print(f"Law III Failures (should be 0): {len(law_III_failures)}")

    if law_III_failures:
        print("\n  [VERDICT: LAW III FALSIFIED]")
        print("  The original PAS Law III does not hold universally.")
    elif total_law_I_failures > 0 :
        print(f"\n  Detailed correlation data saved to: {OUTPUT_CSV_FILE}")
        print("  Analysis of this file is required to determine the relationship")
        print("  between PAC signatures and Law III efficiency (fixing radius r).")
        print("\n  [VERDICT: DATA COLLECTED - ANALYSIS PENDING]")
    else:
         print("\n  No Law I failures found in the test range.")
         print("  [VERDICT: NO DATA TO ANALYZE]")


    print("=" * (50 + len(" PAC-5: PAC-LAW III CORRELATION REPORT ")))

if __name__ == "__main__":
    run_PAC_Law3_correlation_test()