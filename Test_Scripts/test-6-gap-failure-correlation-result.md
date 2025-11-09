# Analysis of Correlation Between $k_{min}$ Failure Type and Anchor Prime Gap $g_n$

**Date:** October 21, 2025

**Author:** Independent Researcher (Valenzuela City, Metro Manila, Philippines)

**Verification Extent:** First 50,000,000 consecutive prime pairs ($p_n, p_{n+1}$)

---

## Abstract

This paper presents the findings of a computational analysis investigating the relationship between "Law I failures" (composite $k_{min}$ distances from an $S_n$ anchor) and the physical construction of the anchor itself, specifically its prime gap $g_n = p_{n+1} - p_n$. The analysis of 6,599,607 failure events over 50 million prime pairs reveals a strong, non-obvious correlation: **composite failures divisible by 3 (e.g., $k=9, 15, 21$) consistently occur at anchors formed from larger-than-average prime gaps**, while **failures _not_ divisible by 3 (e.g., $k=25, 35, 49$) consistently occur at anchors formed from smaller-than-average prime gaps**. This adds a new layer to the Primorial Anchor Conjecture (PAC) framework, demonstrating that $S_n$'s failure modes are linked not only to its modular signature ($S_n \pmod{P_k}$) but also to the spatial arrangement of the primes ($g_n$) that define it.

---

## 1. Background

The Primorial Anchor Conjecture (PAC) successfully established that the arithmetic nature of composite $k_{min}$ failures (where $k_{min} = |S_n - q|$) is deterministically classified by the primorial signature of the anchor $S_n = p_n + p_{n+1}$. This proved a deep connection between the anchor's _modular_ properties and its failure types.

This analysis, `PAC-6`, seeks to determine if a similar connection exists with the anchor's _constructional_ properties. Specifically, it tests for a correlation between the type of composite $k_{min}$ failure and the size of the prime gap $g_n = p_{n+1} - p_n$ that forms the anchor $S_n$.

---

## 2. Methodology

The analysis was conducted using the `run_PAC_failure_gap_correlation()` script.

1.  Anchor points $S_n = p_n + p_{n+1}$ were generated for the first 50,000,000 prime pairs (starting from $n=10$).
2.  For each anchor $S_n$, the associated prime gap $g_n = p_{n+1} - p_n$ was recorded. The overall average gap $\bar{g_n}$ across the entire range was calculated.
3.  "Law I failures" (composite $k_{min}$) were identified by finding the closest prime $q$ to $S_n$.
4.  For each failure event, the composite $k_{min}$ and its associated gap $g_n$ were recorded.
5.  The average gap $g_n(k)$ was calculated for each specific type of composite failure $k_{min}$ and compared to the overall average gap $\bar{g_n}$.

---

## 3. Results

The analysis identified **6,599,607** composite $k_{min}$ failures. The overall average prime gap $g_n$ across the 50,000,000 pairs was **19.6490**.

The data revealed a clear separation: failure types divisible by 3 occurred at significantly larger gaps, while failure types not divisible by 3 occurred at smaller gaps.

### 3.1 Group 1: Failures Divisible by 3 (Occur at Larger Gaps)

These failure types were consistently associated with anchors $S_n$ built from a prime gap $g_n$ **larger** than the overall average.

| $k_{min}$ (Divisible by 3) | Occurrence Count | Avg. Gap Size $g_n(k)$ | % vs. Overall Avg. |
| :------------------------- | :--------------- | :--------------------- | :----------------- |
| 9                          | 2,845,622        | 21.2761                | **+8.28%**         |
| 15                         | 1,252,635        | 21.4030                | **+8.93%**         |
| 21                         | 706,630          | 20.5422                | **+4.55%**         |
| 27                         | 391,464          | 20.1913                | **+2.76%**         |
| 33                         | 181,120          | 20.9542                | **+6.64%**         |
| 45                         | 39,169           | 20.9817                | **+6.78%**         |
| 63                         | 4,982            | 21.4589                | **+9.21%**         |
| 75                         | 1,089            | 22.4628                | **+14.32%**        |

### 3.2 Group 2: Failures Not Divisible by 3 (Occur at Smaller Gaps)

These failure types were consistently associated with anchors $S_n$ built from a prime gap $g_n$ **smaller** than the overall average.

| $k_{min}$ (Not Divisible by 3) | Occurrence Count | Avg. Gap Size $g_n(k)$ | % vs. Overall Avg. |
| :----------------------------- | :--------------- | :--------------------- | :----------------- |
| 25                             | 740,891          | 18.6613                | **-5.03%**         |
| 35                             | 226,689          | 18.8354                | **-4.14%**         |
| 49                             | 46,978           | 18.5018                | **-5.84%**         |
| 55                             | 21,503           | 19.0031                | **-3.29%**         |
| 65                             | 6,720            | 19.1015                | **-2.79%**         |
| 77                             | 1,705            | 18.2733                | **-7.00%**         |
| 85                             | 612              | 19.2222                | **-2.17%**         |

---

## 4. Interpretation and Conclusion

The data provides compelling evidence of a previously unknown correlation: **the arithmetic nature of a $k_{min}$ failure is linked to the physical size of the prime gap $g_n$ that forms the anchor $S_n$.**

This finding deepens the PAC framework. We have now established that the "Law I failures" from the $S_n$ sequence are structurally ordered by two separate, fundamental properties:

1.  **Modular Signature (from PAC):** The $S_n \pmod{P_k}$ value deterministically classifies _which_ failures are arithmetically possible.
2.  **Constructional Signature (from this test):** The $g_n = p_{n+1} - p_n$ value shows a strong statistical correlation with the _type_ of failure that occurs (divisible by 3 vs. not divisible by 3).

This reinforces the conclusion that the $S_n$ sequence is a unique and deeply structured object for analyzing prime distribution. Its failure modes are not random but are constrained and biased by both its modular position ($S_n \pmod{P_k}$) and its physical construction ($g_n$).
