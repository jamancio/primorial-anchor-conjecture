# ==============================================================================
# ANALYSIS SCRIPT: Composite k Distribution (Law I Failure Analysis)
#
# Prime_set creation to include all necessary primes.
#
# This script analyzes the *distribution* of the composite k values
# that cause Law I failures when using the original S_n anchor as the detector.
#
# It answers the question: "When Law I fails, which composite numbers
# (k=9, 15, 21, 25, etc.) are responsible, and what is the frequency
# of each?"
#
# This helps understand the nature of the "messy prime events" that
# the corrective mechanisms (like the Mod 210 system) need to fix.
# ==============================================================================

import math
import time
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt"
# 50M pairs provides a robust statistical sample
MAX_PRIME_PAIRS_TO_TEST = 50000000

# We need a small buffer, but not the full MAX_RADIUS_LIMIT
LOOKUP_BUFFER = 10

# --- Function to load primes from a file ---
def load_primes_from_file(filename):
    """Loads a list of primes from a text file."""
    print(f"Loading primes from {filename}...")
    start_time = time.time()
    try:
        with open(filename, 'r') as f:
            prime_list = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        return None
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes in {end_time - start_time:.2f} seconds.")
    return prime_list

def is_prime(num, prime_set):
    """Checks if a number is prime using the precomputed set."""
    # Ensure we only check positive integers.
    if num < 2:
        return False
    # Check against the set provided.
    return num in prime_set

# --- Main Testing Logic ---
def analyze_k_distribution():

    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    # Need N pairs + the next prime for S_N
    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        # Ensure sufficient primes are loaded to cover the test range.
        print(f"  Need at least {required_primes_count:,} primes.")
        print(f"  Loaded only {len(prime_list):,} primes.")
        return

    # --- *** prime_set CREATION *** ---
    print("\nSafety check passed. Creating prime set for fast lookups...")
    # Use ALL loaded primes for the set to ensure lookups near S_n work
    if not prime_list:
        print("FATAL ERROR: Prime list is empty after loading.")
        return

    prime_set = set(prime_list)
    max_prime_in_set = max(prime_list) if prime_list else 0
    print(f"Prime set created using all {len(prime_set):,} loaded primes (up to {max_prime_in_set:,}). Starting analysis...")


    print(f"\nStarting Composite k Distribution Analysis for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print("-" * 80)
    start_time = time.time()

    # --- Data structures for the analysis ---
    total_law_I_failures = 0
    composite_k_counts = defaultdict(int)

    # Start index from p2+p3 (index 1 in 0-based list)
    start_index = 1

    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            # Update progress status.
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails Found: {total_law_I_failures:,} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        # Check if potential lookups might exceed our loaded primes
        # Add a buffer for the search distance (e.g., 2000)
        max_lookup_needed = anchor_sum + 2000
        if max_lookup_needed > max_prime_in_set:
            print(f"\nFATAL ERROR: Anchor sum plus search distance ({max_lookup_needed:,}) exceeds largest prime in set ({max_prime_in_set:,}) at index {i}.")
            print("Please generate a larger prime file.")
            return # Stop execution if primes are insufficient

        # --- 1. Find the k_min relative to S_n ---
        min_distance_k = 0
        search_dist = 1
        found_prime = 0
        while True:
            # Increased safety break, typical gaps are < 2000 in this range
            if search_dist > 2000:
                # Log warning if search limit is hit, indicating very large gap or issue.
                print(f"\nWarning: Search distance exceeded limit (2000) at index {i} (S_n={anchor_sum:,}). Skipping.")
                min_distance_k = 0 # Ensure this case is skipped
                break

            q_lower = anchor_sum - search_dist
            q_upper = anchor_sum + search_dist

            # Check lower first
            # We use is_prime which checks q_lower > 1 implicitly
            if is_prime(q_lower, prime_set):
                min_distance_k = search_dist
                found_prime = q_lower
                # Now check if upper is ALSO prime at the same distance
                if is_prime(q_upper, prime_set):
                     # If both are equidistant primes, Law I holds (k=prime distance)
                     # The minimum distance *k* itself determines success/failure
                     pass # Continue, k is found
                break

            # Check upper if lower wasn't prime
            if is_prime(q_upper, prime_set):
                min_distance_k = search_dist
                found_prime = q_upper
                break

            search_dist += 1

        if min_distance_k == 0: continue # Skip if search limit hit or other issue

        # --- 2. Check if this k_min constitutes a Law I failure ---
        # Law I holds if k_min is 1 OR if k_min is prime
        # We need to check if min_distance_k itself is in the prime set
        is_law_I_success = (min_distance_k == 1) or is_prime(min_distance_k, prime_set)

        if not is_law_I_success:
            # This is a Law I failure, k_min must be composite
            total_law_I_failures += 1
            composite_k_counts[min_distance_k] += 1

    # Final progress print after loop completion.
    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails Found: {total_law_I_failures:,}   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " Composite k Distribution Report " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")

    if total_law_I_failures == 0:
        print("\nNo Law I failures found.")
        return

    print("\n" + "-"*30 + " Frequency of Composite k Values " + "-"*30)
    print(f"{'Composite k':<15} | {'Count':<20} | {'Percentage':<15}")
    print("-" * 55)

    # Sort items by count (most frequent first)
    sorted_k = sorted(composite_k_counts.items(), key=lambda item: item[1], reverse=True)

    # Print the top 20 most frequent composite k values
    printed_count = 0
    for k, count in sorted_k:
        if printed_count < 20:
            percentage = (count / total_law_I_failures) * 100
            print(f"{k:<15} | {count:<20,} | {percentage:.2f}%")
            printed_count += 1
        else:
            break # Stop after printing top 20

    # Calculate and print remaining count if there are more than 20 unique k values
    if len(sorted_k) > 20:
        remaining_count = sum(count for k, count in sorted_k[20:])
        remaining_percentage = (remaining_count / total_law_I_failures) * 100
        print("-" * 55)
        print(f"{'Other k values':<15} | {remaining_count:<20,} | {remaining_percentage:.2f}%")

    print("-" * 55)
    # Print total line.
    print(f"{'TOTAL':<15} | {total_law_I_failures:<20,} | {100.0:.2f}%")

    print("\n" + "="* (55)) # Match the width of the table separator


if __name__ == "__main__":
    analyze_k_distribution()