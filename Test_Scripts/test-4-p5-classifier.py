# ==============================================================================
# PRIMORIAL ANCHOR CONJECTURE (PAC) - TEST 4: Mod 2310 Verification
#
# This test verifies the PAC prediction specifically for the P_5 = 2310 filter.
#
# METHODOLOGY:
# 1. Use the S_n = p_n + p_{n+1} sequence.
# 2. Find all "Law I Failures" (composite 'k').
# 3. Focus ONLY on anchors where S_n is "perfect" mod 2310 (S_n % 2310 == 0).
# 4. Check if any resulting composite k_min is divisible by 3, 5, 7, or 11.
#
# HYPOTHESIS:
# There should be ZERO violations. Any composite k_min found must NOT be
# divisible by 3, 5, 7, or 11. The first expected failure is k=169 (13^2).
# ==============================================================================

import math
import time
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt"
MAX_PRIME_PAIRS_TO_TEST = 50000000
# Start index safe past p_5 = 11. n=10 (p_10=31) is still fine.
START_INDEX = 10

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
def run_PAC_mod2310_verification():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PAC Mod 2310 Verification for {MAX_PRIME_PAIRS_TO_TEST:,} S_n pairs...")
    print(f"  - Hunting for violations for S_n % 2310 == 0 anchors.")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for the test ---
    total_law_I_failures = 0
    perfect_mod2310_anchors_found = 0
    failures_from_perfect_mod2310 = defaultdict(int) # Store {k_composite: count}
    violations_p5 = [] # Store violation events

    loop_end_index = MAX_PRIME_PAIRS_TO_TEST + START_INDEX
    
    for i in range(START_INDEX, loop_end_index):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - START_INDEX + 1
            print(f"Progress: {progress:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Perfect Anchors: {perfect_mod2310_anchors_found:,} | Violations: {len(violations_p5)}", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_S_n = p_n + p_n_plus_1

        # --- Check if anchor is perfect mod 2310 FIRST ---
        is_perfect_anchor = (anchor_S_n % 2310 == 0)
        if is_perfect_anchor:
            perfect_mod2310_anchors_found += 1

            # --- Find the Law I k_min for this anchor ---
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
                # Increase safety break slightly for rarer anchors
                if search_dist > 3000: break 
            
            if min_distance_k == 0: 
                print(f"\nWarning: Search limit exceeded for perfect anchor S_n={anchor_S_n:,} at index {i}. Skipping.")
                continue 

            # --- Check if it's a composite failure ---
            is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
            
            if is_k_composite:
                total_law_I_failures += 1 # Count overall failures for context
                failures_from_perfect_mod2310[min_distance_k] += 1
                
                failure_event = {
                    "n_index": i, 
                    "S_n": anchor_S_n, 
                    "q_prime": q_prime, 
                    "k_composite": min_distance_k
                }
                
                # --- Check for VIOLATION ---
                # Check divisibility by 3, 5, 7, 11 (prime factors of 2310, excluding 2)
                if (min_distance_k % 3 == 0 or 
                    min_distance_k % 5 == 0 or 
                    min_distance_k % 7 == 0 or 
                    min_distance_k % 11 == 0):
                    violations_p5.append(failure_event)
        else:
            # If not a perfect anchor, still find k_min to count total failures
            min_distance_k = 0
            search_dist = 1
            while True:
                q_lower = anchor_S_n - search_dist
                q_upper = anchor_S_n + search_dist
                if q_lower in prime_set or q_upper in prime_set:
                    min_distance_k = search_dist
                    break
                search_dist += 1
                if search_dist > 2000: break
            
            if min_distance_k > 0:
                 is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
                 if is_k_composite:
                      total_law_I_failures += 1


    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Perfect Anchors: {perfect_mod2310_anchors_found:,} | Violations: {len(violations_p5)}   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " PAC-4: MOD 2310 (P_5) VERIFICATION REPORT " + "="*20)
    print(f"\nTotal S_n Anchors Analyzed: {MAX_PRIME_PAIRS_TO_TEST:,}")
    print(f"Total Law I Failures (Overall): {total_law_I_failures:,}")
    print(f"Total 'Perfect' (S_n % 2310 == 0) Anchors Found: {perfect_mod2310_anchors_found:,}")
    
    total_failures_from_perfect = sum(failures_from_perfect_mod2310.values())
    print(f"\nTotal Composite k Failures from Perfect Anchors: {total_failures_from_perfect:,}")
    
    if failures_from_perfect_mod2310:
        print("  Composite k values observed:")
        for k, count in sorted(failures_from_perfect_mod2310.items()):
            print(f"    - k = {k}: {count:,} instance(s)")
    else:
        print("  No composite k failures were observed from perfect anchors.")

    print(f"\n>>> VIOLATIONS (k % 3, 5, 7, or 11 == 0): {len(violations_p5)}")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if violations_p5:
        print("\n  [VERDICT: CONJECTURE FALSIFIED for P_5]")
        print("  The Primorial Anchor Conjecture failed for P_5 = 2310.")
        print("  We found 'perfect' anchors that produced 'forbidden' k-values.")
        print(f"\n  First P_5 Violation Details: {violations_p5[0]}")
    else:
        print("\n  [VERDICT: CONJECTURE VERIFIED for P_5]")
        print("  The hypothesis is confirmed with 100% accuracy for P_5 across the test range.")
        print("  Perfect S_n % 2310 == 0 anchors produced ZERO failures")
        print("  divisible by 3, 5, 7, or 11.")
        if total_failures_from_perfect > 0:
             print("\n  Observed failures (like k=169+) conform to the prediction.")
        else:
             print("\n  No composite failures were observed from perfect anchors, confirming immunity.")
        print("\n  This further strengthens the PAC.")

    print("=" * (50 + len(" FINAL CONCLUSION ")))

if __name__ == "__main__":
    run_PAC_mod2310_verification()