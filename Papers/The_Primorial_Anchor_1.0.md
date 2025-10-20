# The Primorial Anchor Filter in Local Prime Analysis

**Date:** October 19, 2025

**Author:** Independent Researcher (City of Malabon, Metro Manila, Philippines)

---

## Abstract

This paper introduces the concept of using **Primorial Anchors**, numbers congruent to $0 \pmod{P_{k_th}}$ (where $P_{k_th}$ is the $k$-th primorial), for analyzing the local distribution of prime numbers. It demonstrates mathematically how these anchors act as **Primorial Filters**, placing constraints on the possible arithmetic forms of the distance $k = |Anchor - q|$ to any prime $q$. Computational evidence from large-scale tests (up to 50 million prime pairs) is presented, confirming that the efficiency of finding a "clean" relationship ($k=1$ or $k \in \mathbb{P}$) is directly proportional to the strength of the primorial filter used ($\pmod 2$ vs $\pmod 6$ vs $\pmod{30}$ vs $\pmod{210}$).

---

## 1. Introduction: The Primorial Anchor Concept

The investigation originated from studying the properties of **Anchor Points** defined as $S_n = p_n + p_{n+1}$ (the sum of two consecutive primes). The core idea is to establish such a reference point, an **Anchor**, within the number line to measure its relationship to surrounding primes. The relationship is quantified by the distance $k = |Anchor - q|$, where $q$ is a prime number. The central question is understanding the nature of these distances $k$, specifically the tendency for $k$ to be "clean" ($k=1$ or $k \in \mathbb{P}$).

Initial analysis of $S_n$ anchors revealed they frequently satisfy low-order primorial conditions (e.g., $S_n \equiv 0, 2, \text{ or } 4 \pmod 6$ for $n>1$). This observation led to the generalization of the **Primorial Anchor** concept: using numbers congruent to $0 \pmod{P_{k_th}}$ (where $P_{k_th}$ is the $k$-th primorial) as idealized reference points to understand the underlying filtering mechanism.

While traditional sieve methods use modulo arithmetic to *exclude* numbers from being prime, the **Primorial Anchor** approach uses it to *filter* the possible arithmetic forms of the distance $k$ itself, providing a new perspective on local prime distribution.

---

## 2. The Primorial Filter Mechanism

The key insight is to choose a **Primorial Anchor** such that $Anchor \equiv 0 \pmod{P_{k_th}}$, where $P_{k_th} = 2 \times 3 \times \dots \times p_k$ is the $k$-th primorial. Let $q$ be any prime $q > p_k$. Since $q$ cannot be divisible by any $p_i \le p_k$, $q \not\equiv 0 \pmod{p_i}$.

Consider the distance $k = |Anchor - q|$. Analyzing this modulo $p_i$:
$k \equiv |0 - q| \pmod{p_i}$
$k \equiv |-q| \pmod{p_i}$
Since $q \not\equiv 0 \pmod{p_i}$, it follows that $k \not\equiv 0 \pmod{p_i}$.

This means that by choosing a **Primorial Anchor** $\equiv 0 \pmod{P_{k_th}}$, we **structurally eliminate** any distance $k$ that is divisible by the first $k$ primes.

* **Example 1: $\pmod 6$ Filter ($P_{2_th} = 2 \times 3$)**
    - If $Anchor \equiv 0 \pmod 6$, then $k = |Anchor - q|$ (for $q>3$) cannot be divisible by 2 or 3.
    - $k$ must be of the form $6m \pm 1$.
    - The first possible composite $k$ is $25$ ($5 \times 5$). Failures like $k=9, 15, 21$ are impossible.

* **Example 2: $\pmod{30}$ Filter ($P_{3_th} = 2 \times 3 \times 5$)**
    - If $Anchor \equiv 0 \pmod{30}$, then $k = |Anchor - q|$ (for $q>5$) cannot be divisible by 2, 3, or 5.
    - $k$ must be coprime to 30.
    - The first possible composite $k$ is $49$ ($7 \times 7$). Failures like $k=25, 35, 55$ are now also impossible.

* **Example 3: $\pmod{210}$ Filter ($P_{4_th} = 2 \times 3 \times 5 \times 7$)**
    - If $Anchor \equiv 0 \pmod{210}$, then $k = |Anchor - q|$ (for $q>7$) cannot be divisible by 2, 3, 5, or 7.
    - $k$ must be coprime to 210.
    - The first possible composite $k$ is $121$ ($11 \times 11$). Failures like $k=49, 77, 91$ are now also impossible.

---

## 3. Computational Evidence: Efficiency Hierarchy

A series of large-scale computational tests (analyzing 6.6 million "Law I failures" over 50 million prime pairs) was conducted to measure the efficiency of finding a "clean fix" ($k'=1$ or $k' \in \mathbb{P}$) using different **Primorial Anchor** types. Efficiency was measured by the maximum search depth ($r_{max}$ or $c_{max}$) required to guarantee a 100% correction rate.

The results demonstrated a clear hierarchy directly correlated to the strength of the primorial filter:

| Anchor Filter Type | Filter Strength | Max Search Depth (Efficiency) | $r=1$ / $c=1$ Fix Rate |
| :----------------- | :-------------- | :---------------------------- | :------------------- |
| Random Even        | $\pmod 2$       | $e_{max} \approx 40$          | Low (N/A)            |
| Random Mod 6       | $\pmod 6$       | $c_{max} \approx 20$          | ~84%                 |
| Random Mod 30      | $\pmod{30}$     | $c_{max} \approx 15-19$       | ~90%                 |
| Perfected Mod 210  | $\pmod{210}$    | $r_{max} = 10$                | 94.32%               |

<i>(Note: Random system $c_{max}$ fluctuates; $r=1$ / $c=1$ rates are from specific tests, [r_max Analysis](r-max-analysis.py) )</i>

This data provides strong empirical evidence that increasing the primorial strength of the **Primorial Anchor** significantly reduces the search space for "clean" relationships, thereby increasing the efficiency and reducing the maximum search depth required.

---

## 4. Conclusion

Using **Primorial Anchors** congruent to $0 \pmod{P_{k_th}}$ provides a novel and effective **Primorial Filter** mechanism for analyzing local prime distributions. The strength of the filter directly dictates the set of possible composite distances $k$ that can occur, and computational evidence confirms that stronger filters lead to significantly more efficient searches for "clean" prime relationships. This highlights the deep structural role of small prime factors in governing the local behavior of prime numbers and offers a new perspective beyond traditional sieve methods.