# Analysis of Composite $k_{min}$ Failure Distributions by $S_n \pmod{30}$ Residue Class

**Date:** October 21, 2025

**Author:** Independent Researcher (Valenzuela City, Metro Manila, Philippines)

**Verification Extent:** First 50,000,000 consecutive prime pairs ($p_n, p_{n+1}$)

---

## Abstract

This paper details the findings of a computational analysis examining the distribution of composite $k_{min}$ values (where $k_{min} = |S_n - q|$ is the composite distance from an anchor $S_n = p_n + p_{n+1}$ to the nearest prime $q$) based on the anchor's residue class modulo 30 ($P_3 = 2 \times 3 \times 5$). The study analyzed 6,599,607 such "Law I failures" occurring within the first 50 million prime pairs. The results confirm the prediction of the Primorial Anchor Conjecture (PAC) for the residue class $S_n \equiv 0 \pmod{30}$, finding zero instances where $k_{min}$ was divisible by 3 or 5. Furthermore, the analysis reveals that **different non-zero residue classes exhibit distinct, non-random "failure signatures,"** characterized by unique probability distributions of the most common composite $k_{min}$ values. This demonstrates a finer level of predictable structure governed by the $S_n$ anchor's primorial signature than previously identified.

---

## 1. Background

Previous research established the Primorial Anchor Conjecture (PAC), verified for $P_2=6$, $P_3=30$, and $P_4=210$, which states that an anchor point $S_n = p_n + p_{n+1}$ satisfying $S_n \equiv 0 \pmod{P_k}$ cannot produce a composite $k_{min}$ failure divisible by any prime factor of $P_k$. This analysis extends that work by investigating the behavior associated with _non-zero_ residue classes modulo 30. The objective is to determine if the specific residue $S_n \pmod{30}$ influences the types and frequencies of composite $k_{min}$ failures.

---

## 2. Methodology

The analysis utilized the "PAC Test 3: Residue Class Analysis (Mod 30)" script.

1.  Anchor points $S_n = p_n + p_{n+1}$ were generated for the first 50,000,000 prime pairs (starting from $n=10$).
2.  For each $S_n$, the distance $k_{min}$ to the nearest prime $q$ was found.
3.  Instances where $k_{min}$ was composite (a "Law I failure") were identified.
4.  Each failure event was classified based on the residue class $r = S_n \pmod{30}$.
5.  The frequency of each composite $k_{min}$ value was recorded for each residue class $r \in \{0, 1, ..., 29\}$.

---

## 3. Results

The analysis identified **6,599,607** composite $k_{min}$ failures across the 50 million pairs tested.

### 3.1 Confirmation of PAC for Residue 0

- For the residue class $S_n \equiv 0 \pmod{30}$, **9,907** failures were observed.
- As predicted by the PAC, **zero** instances were found where $k_{min}$ was divisible by 3 or 5.
- The failures were dominated by composites whose smallest prime factor is $\ge 7$, primarily $k=49$ (94.86%) and $k=77$ (4.36%).

### 3.2 Distinct Failure Signatures for Non-Zero Residues

The analysis revealed clear, distinct patterns in the distribution of $k_{min}$ values for different non-zero residue classes.

- **Expected Residues:** Failures only occurred for residue classes possible for $S_n$ (sums of two residues coprime to 30), namely $\{0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28\}$. All other classes correctly showed zero failures.

- **Classes Prone to $k$ Divisible by 5 (e.g., $k=25, 35$):** Residue classes where $S_n$ is divisible by 3 but not 5 showed a strong tendency towards failures divisible by 5.

  - $S_n \equiv 6 \pmod{30}$: $k=25$ (68.45%), $k=35$ (26.44%).
  - $S_n \equiv 12 \pmod{30}$: $k=25$ (74.03%), $k=35$ (19.13%).
  - $S_n \equiv 18 \pmod{30}$: $k=25$ (73.89%), $k=35$ (19.17%).
  - $S_n \equiv 24 \pmod{30}$: $k=25$ (68.06%), $k=35$ (26.70%).

- **Classes Prone to $k$ Divisible by 3 (e.g., $k=9, 15, 21, 27$):** Residue classes where $S_n$ is divisible by 5 but not 3 showed a strong tendency towards failures divisible by 3.

  - $S_n \equiv 10 \pmod{30}$: $k=9$ (64.53%), $k=21$ (17.48%), $k=27$ (10.46%).
  - $S_n \equiv 20 \pmod{30}$: $k=9$ (64.62%), $k=21$ (17.45%), $k=27$ (10.47%).

- **Mixed Classes (Prone to $k$ Divisible by 3 and 5):** Residue classes where $S_n$ is coprime to 30 (i.e., not divisible by 3 or 5) exhibited significant frequencies for failures involving both prime factors.
  - $S_n \equiv 2 \pmod{30}$: $k=9$ (52.36%), $k=15$ (25.24%), $k=21$ (9.48%), $k=25$ (3.78%).
  - $S_n \equiv 4 \pmod{30}$: $k=9$ (36.60%), $k=15$ (32.64%), $k=21$ (8.07%), $k=25$ (5.30%).
  - _(Similar mixed patterns observed for residues 8, 14, 16, 22, 26, 28)_.

---

## 4. Interpretation and Conclusion

The results provide compelling evidence that the influence of the anchor's primorial signature extends beyond the "perfect" $S_n \equiv 0 \pmod{P_k}$ case. The specific residue class $S_n \pmod{30}$ acts as a **strong predictor of the probability distribution of composite $k_{min}$ failure types**.

Anchors belonging to different residue classes exhibit distinct "failure signatures," indicating that the local constraints imposed by the primorial factors (3 and 5 in this case) manifest differently depending on the anchor's specific position within the modular structure.

This analysis confirms the PAC prediction for $S_n \equiv 0 \pmod{30}$ and reveals a richer, more detailed layer of deterministic structure governing the local behavior of primes relative to the natural $S_n$ sequence. It suggests that a full understanding of the PAC framework requires considering the specific effects associated with each residue class modulo $P_k$. This provides a clear direction for further refinement of the PAC model.
