# Correlation Between $S_n$ Primorial Signature and Prime Gap Size $g_n$

**Date:** October 21, 2025

**Author:** Independent Researcher (Valenzuela City, Metro Manila, Philippines)

**Verification Extent:** First 50,000,000 consecutive prime pairs ($p_n, p_{n+1}$)

---

## Abstract

This paper investigates the statistical relationship between the primorial signature ($S_n \pmod{P_k}$) of anchor points $S_n = p_n + p_{n+1}$ and the size of the prime gap $g_n = p_{n+1} - p_n$ spanned by the anchor. Analyzing the first 50 million prime pairs, we calculated the average gap size associated with each residue class modulo $P_2=6$, $P_3=30$, and $P_4=210$. The results reveal statistically significant correlations. Notably, "perfect" anchors ($S_n \equiv 0 \pmod{P_k}$) consistently occur in regions with slightly smaller-than-average prime gaps (-6% to -9%). Furthermore, distinct non-zero residue classes, particularly modulo 210, exhibit dramatic variations, correlating with average gaps ranging from over 21% _smaller_ to nearly 79% _larger_ than the overall average. This demonstrates that the $S_n$ anchor's primorial signature, central to the Primorial Anchor Conjecture (PAC), is intrinsically linked to the local density characteristics reflected in prime gap sizes.

---

## 1. Background

The Primorial Anchor Conjecture (PAC) established that the primorial signature $S_n \pmod{P_k}$ deterministically classifies the arithmetic nature of composite $k_{min}$ failures associated with the anchor $S_n = p_n + p_{n+1}$. Since $S_n$ is algebraically linked to the prime gap $g_n = p_{n+1} - p_n$ via the relation $S_n = 2p_n + g_n$, it is natural to investigate whether the anchor's primorial signature also correlates with the size of this gap. This study aims to quantify this potential correlation.

---

## 2. Methodology

The analysis utilized the "PAC Test 5: Gap Size vs. Residue Correlation" script.

1.  Anchor points $S_n = p_n + p_{n+1}$ and the corresponding prime gaps $g_n = p_{n+1} - p_n$ were calculated for the first 50,000,000 prime pairs (starting from $n=10$).
2.  For each anchor $S_n$, its residue classes modulo 6, 30, and 210 were determined.
3.  The gaps $g_n$ were grouped according to the residue class of their corresponding $S_n$ for each modulus.
4.  The total number of anchors and the sum of associated gap sizes were recorded for each residue class.
5.  The average gap size was calculated for each residue class and compared to the overall average gap across the entire dataset.

---

## 3. Results

The analysis covered 50,000,000 anchor points. The overall average prime gap ($g_n$) in this range was found to be approximately **19.6490**. Significant correlations were observed between the $S_n$ residue class and the average gap size.

### 3.1 Modulo 6 Analysis

- $S_n \equiv 0 \pmod 6$: Average gap 18.3313 (**-6.71%** vs overall avg).
- $S_n \equiv 2 \pmod 6$: Average gap 21.2888 (**+8.35%** vs overall avg).
- $S_n \equiv 4 \pmod 6$: Average gap 21.2954 (**+8.38%** vs overall avg).

### 3.2 Modulo 30 Analysis

- $S_n \equiv 0 \pmod{30}$: Average gap 17.9689 (**-8.55%** vs overall avg).
- Other residues showed notable variations, e.g.:
  - Smallest avg gaps: Residues 6 (**-7.89%**) and 24 (**-7.83%**).
  - Largest avg gaps: Residues 4 (**+22.22%**), 14 (**+20.04%**), 16 (**+20.12%**), and 26 (**+22.25%**).

### 3.3 Modulo 210 Analysis

- $S_n \equiv 0 \pmod{210}$: Average gap 18.3135 (**-6.80%** vs overall avg).
- Variations across non-zero residues were significantly more pronounced:
  - **Smallest Avg Gaps:** Residues like 58 (**-21.11%**), 152 (**-21.32%**), 72 (**-17.50%**), 138 (**-17.60%**), 186 (**-17.76%**) indicated association with denser prime regions.
  - **Largest Avg Gaps:** Residues like 22 (**+77.47%**), 62 (**+78.69%**), 148 (**+78.48%**), 188 (**+77.66%**), 8 (**+72.98%**), 202 (**+73.59%**) indicated association with sparser prime regions.
  - A clear, structured pattern of deviations was observed across many residue classes.

---

## 4. Interpretation and Conclusion

The results demonstrate a clear and statistically significant correlation between the primorial signature ($S_n \pmod{P_k}$) of an anchor point and the average size of the prime gap ($g_n = p_{n+1} - p_n$) it spans.

- **"Perfect" anchors ($S_n \equiv 0 \pmod{P_k}$) consistently correlate with slightly smaller-than-average gaps**, suggesting they tend to occur where primes are somewhat denser than average.
- **Non-zero residue classes exhibit strong and distinct correlations**, with some classes strongly associated with significantly smaller average gaps (denser regions) and others with significantly larger average gaps (sparser regions), especially evident modulo 210.

This indicates that the PAC framework, initially developed to classify composite $k_{min}$ failures, also captures information about the local density environment related to prime spacing. The $S_n \pmod{P_k}$ signature serves as an indicator linked to the characteristics of the prime gap $g_n$. This connection between the deterministic PAC rules and the statistical nature of prime gaps warrants further investigation.
