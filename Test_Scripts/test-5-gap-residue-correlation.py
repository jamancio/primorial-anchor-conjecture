# ==============================================================================
# PRIMORIAL ANCHOR CONJECTURE (PAC) - TEST 5: Gap Size vs. Residue Correlation
#
# This test investigates if the size of the prime gap g_n = p_{n+1} - p_n
# correlates with the residue class of the anchor S_n = p_n + p_{n+1}
# modulo P_k (specifically for P_2=6, P_3=30, and P_4=210).
#
# GOAL:
# Determine if the average gap size differs significantly for anchors
# belonging to different residue classes (e.g., is the average gap
# different when S_n % 210 == 0 compared to when S_n % 210 == 2?).
# ==============================================================================

import math
import time
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt"
MAX_PRIME_PAIRS_TO_TEST = 50000000
# Start index safe past p_4 = 7. n=10 (p_10=31) is still fine.
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
        return None
    
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes in {end_time - start_time:.2f} seconds.")
    
    # Need N pairs + the next prime for S_N
    required_primes = MAX_PRIME_PAIRS_TO_TEST + START_INDEX + 1
    if len(prime_list) < required_primes:
        print(f"\nFATAL ERROR: Prime file is too small.")
        print(f"  Need {required_primes:,} primes, found {len(prime_list):,}.")
        return None
        
    return prime_list

# --- Main Testing Logic ---
def run_PAC_gap_residue_correlation():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PAC Gap Size vs. Residue Correlation for {MAX_PRIME_PAIRS_TO_TEST:,} S_n pairs...")
    print(f"  - Calculating average gap g_n for each S_n % P_k class (k=2,3,4).")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for the test ---
    # Store {residue: {'count': N, 'gap_sum': total_gap}}
    gap_stats_mod6 = {i: {'count': 0, 'gap_sum': 0} for i in range(6)}
    gap_stats_mod30 = {i: {'count': 0, 'gap_sum': 0} for i in range(30)}
    gap_stats_mod210 = {i: {'count': 0, 'gap_sum': 0} for i in range(210)}
    
    total_anchors_analyzed = 0
    
    loop_end_index = MAX_PRIME_PAIRS_TO_TEST + START_INDEX
    
    for i in range(START_INDEX, loop_end_index):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - START_INDEX + 1
            print(f"Progress: {progress:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_S_n = p_n + p_n_plus_1
        gap_g_n = p_n_plus_1 - p_n
        total_anchors_analyzed += 1

        # --- Calculate Residues ---
        residue_mod6 = anchor_S_n % 6
        residue_mod30 = anchor_S_n % 30
        residue_mod210 = anchor_S_n % 210

        # --- Accumulate Stats ---
        gap_stats_mod6[residue_mod6]['count'] += 1
        gap_stats_mod6[residue_mod6]['gap_sum'] += gap_g_n

        gap_stats_mod30[residue_mod30]['count'] += 1
        gap_stats_mod30[residue_mod30]['gap_sum'] += gap_g_n

        gap_stats_mod210[residue_mod210]['count'] += 1
        gap_stats_mod210[residue_mod210]['gap_sum'] += gap_g_n
            
    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Time: {time.time() - start_time:.0f}s   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Calculate Overall Average Gap ---
    total_gap_sum = sum(stats['gap_sum'] for stats in gap_stats_mod6.values())
    overall_avg_gap = total_gap_sum / total_anchors_analyzed if total_anchors_analyzed > 0 else 0

    # --- Final Reports ---
    print("\n" + "="*20 + " PAC-5: GAP SIZE vs. RESIDUE CORRELATION REPORT " + "="*20)
    print(f"\nTotal S_n Anchors Analyzed: {total_anchors_analyzed:,}")
    print(f"Overall Average Prime Gap (g_n) in Range: {overall_avg_gap:.4f}")

    # --- Function to Print Table ---
    def print_residue_report(modulus, gap_stats, overall_avg):
        print("\n" + "-" * 20 + f" Analysis for Mod {modulus} " + "-" * 20)
        print(f"{'Residue':<10} | {'Anchor Count':<15} | {'Avg Gap Size':<15} | {'vs Overall':<15}")
        print("-" * 60)
        
        sorted_residues = sorted(gap_stats.keys())
        
        for residue in sorted_residues:
            stats = gap_stats[residue]
            count = stats['count']
            if count == 0:
                # Optionally skip printing residues that never occur
                # print(f"{residue:<10} | {0:<15,} | {'N/A':<15} | {'N/A':<15}")
                continue 
                
            gap_sum = stats['gap_sum']
            avg_gap = gap_sum / count
            diff_percent = ((avg_gap / overall_avg) - 1) * 100 if overall_avg > 0 else 0
            
            print(f"{residue:<10} | {count:<15,} | {avg_gap:<15.4f} | {diff_percent:+.2f}%")
        print("-" * 60)

    # --- Print Reports for Mod 6, 30, 210 ---
    print_residue_report(6, gap_stats_mod6, overall_avg_gap)
    print_residue_report(30, gap_stats_mod30, overall_avg_gap)
    print_residue_report(210, gap_stats_mod210, overall_avg_gap)

    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    print("\n  Analysis complete. Review the average gap sizes above.")
    print("  Look for statistically significant deviations (+/- %) for specific residues,")
    print("  especially the 'perfect' residue (0) for each modulus.")
    print("  Does S_n % P_k == 0 correlate with larger or smaller average gaps?")

    print("=" * (50 + len(" FINAL CONCLUSION ")))

if __name__ == "__main__":
    run_PAC_gap_residue_correlation()