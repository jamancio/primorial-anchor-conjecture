# ==============================================================================
# PRIMORIAL ANCHOR CONJECTURE (PAC) - TEST 1
#
# METHODOLOGY:
# 2. We loop through every prime 'q' in the test range.
# 3. For each 'q', we find the SINGLE CLOSEST anchor from each
#    ideal P_k grid (multiples of 6, 30, and 210).
# 4. We calculate the distance k = |A_k - q|.
# 5. We ask ONE question: "Is k composite?" (Yes/No).
# 6. We measure the total "Composite Failure Rate" (CFR) for each system.
#
# CONJECTURE: CFR(P_4) < CFR(P_3) < CFR(P_2)
# ==============================================================================

import time
import math
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
MAX_PRIMES_TO_TEST = 50000000 # Use the first 50M primes

# --- Function to load primes ---
def load_primes_from_file(filename, max_count):
    print(f"Loading primes from {filename}...")
    start_time = time.time()
    prime_list = []
    try:
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i >= max_count:
                    break
                prime_list.append(int(line.strip()))
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        return None, None
    
    prime_set = set(prime_list)
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes and created set in {end_time - start_time:.2f} seconds.")
    return prime_list, prime_set

# --- Helper function for the test ---
def get_closest_anchor(q, primorial):
    """Finds the closest multiple of the primorial to q."""
    # (q // primorial) * primorial -> gives the multiple *below* q
    # We must also check the multiple *above* q.
    
    A_below = (q // primorial) * primorial
    A_above = A_below + primorial
    
    if (q - A_below) < (A_above - q):
        return A_below
    else:
        return A_above

# --- Main Testing Logic ---
def run_PAC_CFR_test():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE, MAX_PRIMES_TO_TEST)
    if prime_list is None: return

    print(f"\nStarting PAC Composite Failure Rate (CFR) Test...")
    print(f"Testing {len(prime_list):,} total primes.")
    print("-" * 80)
    start_time = time.time()

    # --- Data structures for the CFR Test ---
    # We will count the total number of composite k's found for each system.
    # We skip the first few primes (2, 3, 5, 7) for a fair test.
    primes_to_test = [p for p in prime_list if p > 7]
    total_primes_tested = len(primes_to_test)
    
    failure_counts = {
        6: 0,   # P_2
        30: 0,  # P_3
        210: 0  # P_4
    }

    # --- Loop through every prime 'q' ---
    for i, q in enumerate(primes_to_test):
        
        if (i + 1) % 100000 == 0:
            print(f"Progress: {i+1:,} / {total_primes_tested:,}", end='\r')

        # --- Test System P_2 (Mod 6) ---
        A_6 = get_closest_anchor(q, 6)
        k_6 = abs(A_6 - q)
        if (k_6 > 1) and (k_6 not in prime_set):
            failure_counts[6] += 1

        # --- Test System P_3 (Mod 30) ---
        A_30 = get_closest_anchor(q, 30)
        k_30 = abs(A_30 - q)
        if (k_30 > 1) and (k_30 not in prime_set):
            failure_counts[30] += 1

        # --- Test System P_4 (Mod 210) ---
        A_210 = get_closest_anchor(q, 210)
        k_210 = abs(A_210 - q)
        if (k_210 > 1) and (k_210 not in prime_set):
            failure_counts[210] += 1

    print(f"Progress: {total_primes_tested:,} / {total_primes_tested:,}   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " PAC-1: COMPOSITE FAILURE RATE (CFR) REPORT " + "="*20)
    print(f"Total Primes Analyzed (q > 7): {total_primes_tested:,}")

    # Calculate percentages
    cfr_6 = (failure_counts[6] / total_primes_tested) * 100
    cfr_30 = (failure_counts[30] / total_primes_tested) * 100
    cfr_210 = (failure_counts[210] / total_primes_tested) * 100

    print("\n" + "-"*20 + " Failure Rate by Primorial Filter " + "-"*20)
    print(f"  System P_2 (Mod 6):    {cfr_6:.4f}%  ({failure_counts[6]:,} failures)")
    print(f"  System P_3 (Mod 30):   {cfr_30:.4f}%  ({failure_counts[30]:,} failures)")
    print(f"  System P_4 (Mod 210):  {cfr_210:.4f}%  ({failure_counts[210]:,} failures)")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if cfr_210 < cfr_30 and cfr_30 < cfr_6:
        print("\n  [VERDICT: CONJECTURE VERIFIED]")
        print("  The deterministic decay of the failure rate is confirmed.")
        print("  CFR(P_4) < CFR(P_3) < CFR(P_2)")
        print("\n  This provides powerful empirical evidence for the")
        print("  Primorial Anchor Conjecture (PAC).")
    else:
        print("\n  [VERDICT: CONJECTURE FALSIFIED]")
        print("  The predicted decay was not observed.")
        print("  The relationship between filter strength and failure rate is not")
        print("  a simple monotonic decay.")

    print("=" * (50 + len(" FINAL CONCLUSION ")))

if __name__ == "__main__":
    run_PAC_CFR_test()