# ==============================================================================
# PRIMORIAL ANCHOR CONJECTURE (PAC) - TEST 2
#
# Definitive test of the Primorial Anchor Conjecture.
#
# METHODOLOGY:
# 1. We use the S_n = p_n + p_{n+1} sequence as the object of study.
# 2. We find every "Law I Failure" (composite 'k').
# 3. For each failure, we test our core hypothesis against
#    P_2 (6), P_3 (30), and P_4 (210).
#
# CORE HYPOTHESIS:
# An anchor S_n % P_k == 0 will NEVER produce a failure 'k'
# that is divisible by any of the prime factors of P_k.
#
# CORRECTION:
#   a complete 'prime_set'. This is necessary for the
#   'q_prime in prime_set' check to be logically valid when
#   S_n becomes larger than p_{50,000,000}.
# ==============================================================================

import math
import time
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
MAX_PRIME_PAIRS_TO_TEST = 50000000
START_INDEX = 10 

# --- Function to load primes from a file ---
def load_primes_from_file(filename):
    """
    Loads ALL primes from the text file.
    This is critical for the 'in prime_set' check to work
    for large S_n anchors.
    """
    print(f"Loading ALL primes from {filename}...")
    print("(This may take a moment and consume significant RAM)")
    start_time = time.time()
    try:
        with open(filename, 'r') as f:
            prime_list = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        return None, None
    
    # We create the set from the *entire* list of primes
    prime_set = set(prime_list)
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes and created set in {end_time - start_time:.2f} seconds.")
    
    # Now, check if we have enough primes for the requested test
    required_primes = MAX_PRIME_PAIRS_TO_TEST + START_INDEX + 10
    if len(prime_list) < required_primes:
        print(f"\nFATAL ERROR: Prime file is too small.")
        print(f"  Need {required_primes:,} primes, but file only has {len(prime_list):,}.")
        return None, None
        
    return prime_list, prime_set

# --- Main Testing Logic ---
def run_PAC_classifier_suite():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PAC Classifier Suite for {MAX_PRIME_PAIRS_TO_TEST:,} S_n pairs...")
    print(f"  - Testing S_n anchors from p_n={prime_list[START_INDEX]}...")
    print(f"  - Hunting for violations of the Primorial Filter hypothesis.")
    print("-" * 80)
    start_time = time.time()
    
    total_law_I_failures = 0
    
    violations_p2 = [] # S_n % 6 == 0 but k % 3 == 0
    violations_p3 = [] # S_n % 30 == 0 but (k % 3 == 0 or k % 5 == 0)
    violations_p4 = [] # S_n % 210 == 0 but (k % 3 == 0, k % 5 == 0, or k % 7 == 0)

    p2_failures_by_k = defaultdict(int) # k values from S_n % 6 == 0
    p3_failures_by_k = defaultdict(int) # k values from S_n % 30 == 0
    p4_failures_by_k = defaultdict(int) # k values from S_n % 210 == 0
    
    # Main loop
    loop_end_index = MAX_PRIME_PAIRS_TO_TEST + START_INDEX
    
    for i in range(START_INDEX, loop_end_index):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - START_INDEX + 1
            print(f"Progress: {progress:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Violations: {len(violations_p4)} | Time: {elapsed:.0f}s", end='\r')

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

            # We must check 'q_lower' first, as it's the
            # canonical "closest" prime in a tie.
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
        # NOTE: k > 1 is implicit since search_dist starts at 1
        # and we only get here if k is not in prime_set.
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            total_law_I_failures += 1
            
            failure_event = {
                "n_index": i, 
                "S_n": anchor_S_n, 
                "q_prime": q_prime, 
                "k_composite": min_distance_k
            }
            
            # --- 3. Run the Classifier Suite ---
            k_mod_3 = (min_distance_k % 3 == 0)
            k_mod_5 = (min_distance_k % 5 == 0)
            k_mod_7 = (min_distance_k % 7 == 0)

            # --- P2 (Mod 6) Test ---
            if anchor_S_n % 6 == 0:
                p2_failures_by_k[min_distance_k] += 1
                if k_mod_3:
                    violations_p2.append(failure_event)

            # --- P3 (Mod 30) Test ---
            if anchor_S_n % 30 == 0:
                p3_failures_by_k[min_distance_k] += 1
                if k_mod_3 or k_mod_5:
                    violations_p3.append(failure_event)

            # --- P4 (Mod 210) Test ---
            if anchor_S_n % 210 == 0:
                p4_failures_by_k[min_distance_k] += 1
                if k_mod_3 or k_mod_5 or k_mod_7:
                    violations_p4.append(failure_event)

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Violations: {len(violations_p4)} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " PAC-2: CLASSIFIER SUITE REPORT " + "="*20)
    print(f"\nTotal S_n Anchors Analyzed: {MAX_PRIME_PAIRS_TO_TEST:,}")
    print(f"Total Law I Failures (Composite k) Found: {total_law_I_failures:,}")

    # --- P2 (Mod 6) Report ---
    print("\n" + "-"*20 + " P_2 (Mod 6) Filter Analysis " + "-"*20)
    print(f"  Total failures from 'perfect' (S_n % 6 == 0) anchors: {sum(p2_failures_by_k.values()):,}")
    print(f"  Unique k-values seen: {sorted(p2_failures_by_k.keys())[:10]}...")
    print(f"  >>> VIOLATIONS (k % 3 == 0): {len(violations_p2)}")

    # --- P3 (Mod 30) Report ---
    print("\n" + "-"*20 + " P_3 (Mod 30) Filter Analysis " + "-"*20)
    print(f"  Total failures from 'perfect' (S_n % 30 == 0) anchors: {sum(p3_failures_by_k.values()):,}")
    print(f"  Unique k-values seen: {sorted(p3_failures_by_k.keys())[:10]}...")
    print(f"  >>> VIOLATIONS (k % 3 == 0 or k % 5 == 0): {len(violations_p3)}")
    
    # --- P4 (Mod 210) Report ---
    print("\n" + "-"*20 + " P_4 (Mod 210) Filter Analysis " + "-"*20)
    print(f"  Total failures from 'perfect' (S_n % 210 == 0) anchors: {sum(p4_failures_by_k.values()):,}")
    print(f"  Unique k-values seen: {sorted(p4_failures_by_k.keys())[:10]}...")
    print(f"  >>> VIOLATIONS (k % 3, 5, or 7 == 0): {len(violations_p4)}")

    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if violations_p2 or violations_p3 or violations_p4:
        print("\n  [VERDICT: CONJECTURE FALSIFIED]")
        print("  The Primorial Anchor Conjecture has been Falsified.")
        print("  We found 'perfect' anchors that produced 'forbidden' k-values.")
        print("\n  VIOLATION SUMMARY:")
        print(f"  - P_2 (Mod 6) Violations: {len(violations_p2)}")
        print(f"  - P_3 (Mod 30) Violations: {len(violations_p3)}")
        print(f"  - P_4 (Mod 210) Violations: {len(violations_p4)}")
        
        if violations_p4:
             print(f"\n  First P_4 Violation Details: {violations_p4[0]}")
    else:
        print("\n  [VERDICT: CONJECTURE VERIFIED]")
        print("  The hypothesis is confirmed with 100% accuracy across the test range.")
        print("  The S_n anchor's primorial signature *perfectly* predicts")
        print("  the arithmetic nature of its composite k failures.")
        print("\n  VIOLATION SUMMARY:")
        print("  - P_2 (Mod 6) Violations: 0")
        print("  - P_3 (Mod 30) Violations: 0")
        print("  - P_4 (Mod 210) Violations: 0")
        print("\n  This is a significant structural finding.")

    print("=" * (50 + len(" FINAL CONCLUSION ")))

if __name__ == "__main__":
    run_PAC_classifier_suite()