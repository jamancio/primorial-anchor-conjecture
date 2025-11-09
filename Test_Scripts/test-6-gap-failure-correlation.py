# ==============================================================================
# PRIMORIAL ANCHOR CONJECTURE (PAC) - TEST 6: Failure Type vs. Gap Correlation
#
# This test investigates if the specific composite value k_min that causes
# a Law I failure correlates with the size of the prime gap g_n = p_{n+1} - p_n
# associated with the failing anchor S_n = p_n + p_{n+1}.
#
# GOAL:
# Determine if the average gap size g_n is statistically different for
# anchors that produce k=9 failures compared to those producing k=25, k=49, etc.
# ==============================================================================

import math
import time
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt"
MAX_PRIME_PAIRS_TO_TEST = 50000000
START_INDEX = 10 # Consistent start

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
    
    required_primes = MAX_PRIME_PAIRS_TO_TEST + START_INDEX + 10 # Need buffer for Sn+1
    if len(prime_list) < required_primes:
        print(f"\nFATAL ERROR: Prime file is too small.")
        return None, None
        
    return prime_list, prime_set

# --- Main Testing Logic ---
def run_PAC_failure_gap_correlation():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PAC Failure Type vs. Gap Correlation for {MAX_PRIME_PAIRS_TO_TEST:,} S_n pairs...")
    print(f"  - Calculating average gap g_n associated with each composite k_min failure type.")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for the test ---
    total_law_I_failures = 0
    # Store {k_composite: {'count': N, 'gap_sum': total_gap}}
    gap_stats_by_k = defaultdict(lambda: {'count': 0, 'gap_sum': 0})
    
    total_gap_sum_overall = 0 # To calculate overall average gap
    total_anchors_analyzed = 0
    
    loop_end_index = MAX_PRIME_PAIRS_TO_TEST + START_INDEX
    
    for i in range(START_INDEX, loop_end_index):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - START_INDEX + 1
            print(f"Progress: {progress:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_S_n = p_n + p_n_plus_1
        gap_g_n = p_n_plus_1 - p_n
        
        total_anchors_analyzed += 1
        total_gap_sum_overall += gap_g_n

        # --- Find the Law I k_min ---
        min_distance_k = 0
        search_dist = 1
        
        while True:
            q_lower = anchor_S_n - search_dist
            q_upper = anchor_S_n + search_dist

            if q_lower in prime_set:
                min_distance_k = search_dist
                break
            if q_upper in prime_set:
                min_distance_k = search_dist
                break
                
            search_dist += 1
            if search_dist > 2000: break 
        
        if min_distance_k == 0: continue 

        # --- Check if it's a composite failure ---
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            total_law_I_failures += 1
            
            # --- Record the gap associated with this k_min value ---
            gap_stats_by_k[min_distance_k]['count'] += 1
            gap_stats_by_k[min_distance_k]['gap_sum'] += gap_g_n
            
    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Time: {time.time() - start_time:.0f}s   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Calculate Overall Average Gap ---
    overall_avg_gap = total_gap_sum_overall / total_anchors_analyzed if total_anchors_analyzed > 0 else 0

    # --- Final Reports ---
    print("\n" + "="*20 + " PAC-6: FAILURE TYPE vs. GAP CORRELATION REPORT " + "="*20)
    print(f"\nTotal S_n Anchors Analyzed: {total_anchors_analyzed:,}")
    print(f"Total Law I Failures Found: {total_law_I_failures:,}")
    print(f"Overall Average Prime Gap (g_n) in Range: {overall_avg_gap:.4f}")

    print("\n" + "-" * 20 + " Average Gap (g_n) by Composite Failure Type (k_min) " + "-" * 20)
    print(f"{'Comp k_min':<12} | {'Occurrence Count':<18} | {'Avg Gap Size (g_n)':<20} | {'vs Overall':<15}")
    print("-" * 70)
    
    # Sort k values by occurrence count (most frequent first)
    sorted_k_stats = sorted(gap_stats_by_k.items(), key=lambda item: item[1]['count'], reverse=True)
    
    # Print stats for the top 20 most frequent composite k values
    printed_count = 0
    for k, stats in sorted_k_stats:
        if printed_count >= 20:
             break
             
        count = stats['count']
        if count == 0: continue # Should not happen, but safety check
            
        gap_sum = stats['gap_sum']
        avg_gap = gap_sum / count
        diff_percent = ((avg_gap / overall_avg_gap) - 1) * 100 if overall_avg_gap > 0 else 0
        
        print(f"{k:<12} | {count:<18,} | {avg_gap:<20.4f} | {diff_percent:+.2f}%")
        printed_count += 1

    # Optionally, summarize the rest
    if len(sorted_k_stats) > 20:
        remaining_count = sum(stats['count'] for k, stats in sorted_k_stats[20:])
        remaining_gap_sum = sum(stats['gap_sum'] for k, stats in sorted_k_stats[20:])
        if remaining_count > 0:
             avg_gap_remaining = remaining_gap_sum / remaining_count
             diff_percent_remaining = ((avg_gap_remaining / overall_avg_gap) - 1) * 100 if overall_avg_gap > 0 else 0
             print("-" * 70)
             print(f"{'Other k':<12} | {remaining_count:<18,} | {avg_gap_remaining:<20.4f} | {diff_percent_remaining:+.2f}%")
        
    print("-" * 70)

    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    print("\n  Analysis complete. Review the average gap sizes for each k_min type.")
    print("  Look for statistically significant differences in the average gap")
    print("  associated with the most common failure types (e.g., k=9 vs k=25).")
    print("  Does the type of local failure (k_min) correlate with the spacing (g_n)")
    print("  of the primes forming the anchor where the failure was detected?")

    print("=" * (50 + len(" FINAL CONCLUSION ")))

if __name__ == "__main__":
    run_PAC_failure_gap_correlation()