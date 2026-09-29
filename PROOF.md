# PROOF.md — rigorous progress on OEIS A060957 (Yan Sheng Ang's conjecture)

Running file. Everything in Parts I–III is proved in full. Part IV states **exactly** what is still
open, and Part V records strengthenings that are **false** (with explicit counterexamples) so nobody
builds on them. Evidence numbers refer to scripts in `scripts/session2/`.

Status line (update on every commit): **conjecture NOT yet proved.** The whole conjecture is now
reduced (rigorously) to two statements, (L\*) and (B), about "class 𝒞" worlds (Part III, Theorem 3.9).
Lemma L for prime powers x = q^k is now *proved* inside the induction (it was open before).

---

## Part I. Setup and the reduction to intervals of reps

Throughout, n ≥ 1 and p ≤ n is prime. P_n = { ∏S : S ⊆ [1..n] }.
Every positive integer is uniquely R·p^e with p ∤ R. For p-free R put

  E_n(R) = { e ≥ 0 : R·p^e ∈ P_n }.

**Lemma 1.1.** The conjecture for (n, p) ⇔ E_n(R) is an integer interval (possibly empty) for every p-free R.

*Proof.* (⇐) m, p^a m ∈ P_n; write m = R p^{e0}. Then e0, e0+a ∈ E_n(R), so e0+k ∈ E_n(R) for 0<k<a.
(⇒) e1 < e < e2 with e1, e2 ∈ E_n(R): apply the conjecture to m = R p^{e1}, a = e2−e1, k = e−e1. ∎

**Chains.** For p-free r ≥ 1 let C_r = { r p^i : i ≥ 0, r p^i ≤ n }, ℓ_r = |C_r|. The C_r partition
[1..n]. For r = 1, C_1 = {1, p, …, p^L}, L = ⌊log_p n⌋. Let W_n = { r ∈ [2, n] : p ∤ r }.

A subset S ⊆ [1..n] is determined by the sets A_r = { i : r p^i ∈ S } ⊆ [0, ℓ_r − 1], and
∏S = ∏_{r≥2} r^{|A_r|} · p^{Σ_r Σ_{i∈A_r} i}. (The element 1 is irrelevant.)

A **rep** of R is a vector e = (e_r)_{r ∈ W_n} with 0 ≤ e_r ≤ ℓ_r and ∏ r^{e_r} = R.

**Lemma 1.2 (fixed-size subset sums).** For 0 ≤ k ≤ ℓ, { Σ_{i∈A} i : A ⊆ [0, ℓ−1], |A| = k } is the
interval [C(k,2), C(ℓ,2) − C(ℓ−k,2)].

*Proof.* The bottom set {0..k−1} and top set {ℓ−k..ℓ−1} give the endpoints. If A ≠ top set, some i ∈ A has
i+1 ≤ ℓ−1, i+1 ∉ A (otherwise A is closed upward in [0, ℓ−1], i.e. the top set); replacing i by i+1
raises the sum by exactly 1. Hence every value between the endpoints occurs. ∎

**Lemma 1.3.** The subset sums of {1, …, L} are exactly [0, T0], T0 = L(L+1)/2.

*Proof.* Induction on L: sums for {1..L−1} are [0, C(L,2)]; adding L gives [L, C(L+1,2)]; these overlap
or touch since L ≤ C(L,2) + 1 ⇔ (L−1)(L−2) ≥ 0. ∎

**Lemma 1.4 (decomposition).** E_n(R) = ⋃_{e rep of R} ( [lo(e), hi(e)] + [0, T0] ), where
lo(e) = Σ_r C(e_r, 2), hi(e) = Σ_r [C(ℓ_r,2) − C(ℓ_r−e_r,2)].

*Proof.* Choose the counts e_r = |A_r| first; by Lemma 1.2 each chain independently contributes any value
of its interval, the pure chain contributes [0, T0] by Lemma 1.3, and Minkowski sums of integer
intervals are integer intervals. ∎

Note hi(e) − lo(e) = Σ_r e_r (ℓ_r − e_r).

**Lemma 1.5 (P1).** For reps e, f of R: lo(f) ≤ hi(e) + Σ_{r : f_r > e_r} C(f_r − e_r, 2).

*Proof.* Put a_r = f_r − e_r. If a_r > 0 then C(f_r,2) − C(e_r,2) = a_r e_r + C(a_r,2); if a_r ≤ 0 it is ≤ 0.
So lo(f) − lo(e) ≤ Σ_{a_r>0} (a_r e_r + C(a_r,2)). Since f_r ≤ ℓ_r, a_r ≤ ℓ_r − e_r, hence
hi(e) − lo(e) = Σ e_r(ℓ_r − e_r) ≥ Σ_{a_r>0} e_r a_r. Combine. ∎

**Lemma 1.6 (slack).** For r ∈ W_n, C(ℓ_r, 2) ≤ T0.

*Proof.* r p^{ℓ_r−1} ≤ n and r ≥ 2 give p^{ℓ_r−1} ≤ n/2 < n, so ℓ_r − 1 ≤ L and C(ℓ_r,2) ≤ C(L+1,2) = T0. ∎

**Definition 1.7 (M-adjacent).** Two count vectors e, f are *M-adjacent* if at most one coordinate has
f_r − e_r ≥ 2 and at most one coordinate has e_r − f_r ≥ 2.

**Lemma 1.8.** If e, f are M-adjacent reps of R then [lo(e), hi(e)+T0] ∩ [lo(f), hi(f)+T0] ≠ ∅.

*Proof.* By P1, only the (at most one) coordinate with a_r ≥ 2 contributes, so
lo(f) ≤ hi(e) + C(ℓ_r,2) ≤ hi(e) + T0 by Lemma 1.6; symmetrically lo(e) ≤ hi(f) + T0.
Two integer intervals [a,b], [c,d] with c ≤ b and a ≤ d intersect. ∎

**Theorem 1.9 (MC ⇒ conjecture).** If for every R the reps of R are connected under M-adjacency (MC),
then every E_n(R) is an interval, so the conjecture holds for (n, p).

*Proof.* Order the reps along a spanning tree of the M-graph; each new interval meets an earlier one
(Lemma 1.8), so the running union stays an interval. Conclude with Lemmas 1.4 and 1.1. ∎

---

## Part II. General chain decomposition (any prime q, any divisor-closed world)

Let V be a finite set of integers ≥ 2 that is **divisor-closed** (every divisor > 1 of an element of V is
in V), with caps c : V → ℤ_{≥1}. A *rep* of M over (V, c) is a count vector with ∏ v^{e_v} = M,
0 ≤ e_v ≤ c_v; R_V(M) is the set of reps, S(V, c) = { M : R_V(M) ≠ ∅ }.

Fix a prime q. For q-free u ∈ V the **q-chain** of u is { u q^i ∈ V }; by divisor-closedness its level set
is an initial segment [0, h_u]. The pure chain is { q^i ∈ V, i ≥ 1 } = levels [1, h_1].
Let V_{q'} = { u ∈ V : q ∤ u } (divisor-closed) with caps κ_u = Σ_{i=0}^{h_u} c_{u q^i}.
Let Λ_u be the multiset in which level i occurs c_{u q^i} (≥ 1) times, and put
lo_u(k) = sum of the k smallest elements of Λ_u, hi_u(k) = sum of the k largest (0 ≤ k ≤ κ_u),
T_q = Σ_{i=1}^{h_1} i · c_{q^i}.

**Lemma 2.1.** For 0 ≤ k ≤ |Λ|, the sums of k-element sub-multisets of a multiset Λ in which every level
0, …, h occurs at least once form the interval [lo(k), hi(k)]. The sums of *all* sub-multisets of a
multiset in which every level 1, …, h occurs at least once form [0, total].

*Proof.* First claim: if a sub-multiset A is not the top one, pick levels i < j with A using a copy at i
and leaving a copy at j free, with j − i minimal; minimality forces j = i+1 (level i+1 is present, and it is
either partly free or fully used), and moving that copy from i to i+1 raises the sum by 1. Second claim:
sort the multiset; each element is ≤ 1 + (sum of the smaller ones), since levels 1..h all occur; the
standard induction gives every value in [0, total]. ∎

**Lemma 2.2 (q-decomposition).** For M with q ∤ M:
{ e : M q^e ∈ S(V, c) } = ⋃_{m ∈ R_{V_{q'}}(M) with caps κ} ( [lo(m), hi(m)] + [0, T_q] ),
lo(m) = Σ_u lo_u(m_u), hi(m) = Σ_u hi_u(m_u).

*Proof.* A rep of M q^e is the same as: a count m_u ≤ κ_u of blocks in each chain u (their product being M),
a placement of those m_u blocks on levels respecting the per-level caps, and a sub-multiset of the pure
chain; the q-exponent is the sum of all levels. Apply Lemma 2.1 per chain and add intervals. ∎

**Lemma 2.3 (generalized P1).** For core vectors m, m' ∈ R_{V_{q'}}(M):
lo(m') ≤ hi(m) + Σ_{u : m'_u > m_u} lo_u(m'_u − m_u).

*Proof.* Per chain. If m'_u ≤ m_u: lo_u(m'_u) ≤ lo_u(m_u) ≤ hi_u(m_u). If m'_u = a + d > a = m_u, let
λ_1 ≤ … ≤ λ_K be Λ_u sorted (K = κ_u ≥ a + d). Since K − a + i ≥ d + i, λ_{K−a+i} ≥ λ_{d+i}, so
lo_u(a+d) − hi_u(a) = Σ_{i≤a+d} λ_i − Σ_{i≤a} λ_{K−a+i} ≤ Σ_{i≤a+d} λ_i − Σ_{i≤a} λ_{d+i} = Σ_{i≤d} λ_i = lo_u(d). ∎

**Definition 2.4 (domination).** (V, c) is *q-dominated* if Σ_{i≥1} i c_{u q^i} ≤ T_q for every q-free u ∈ V.
(Then lo_u(d) ≤ lo_u(κ_u) = Σ_i i c_{uq^i} ≤ T_q for every d.)

**Theorem 2.5 (fibers along a prime).** If (V, c) is q-dominated and MC holds for (V_{q'}, κ), then for
every M the set { e : M q^e ∈ S(V, c) } is an interval ("G\* along q").

*Proof.* For M-adjacent core vectors, Lemma 2.3 gives lo(m') ≤ hi(m) + lo_u(d) ≤ hi(m) + T_q for the at
most one u with difference d ≥ 2 (a difference 1 contributes lo_u(1) = 0 because level 0 is present).
Symmetrically, so the intervals of Lemma 2.2 meet; conclude as in Theorem 1.9. ∎

(Part I is exactly the case V = W_n, q = p, c = ℓ; there T_q = T0 and domination is Lemma 1.6.)

---

## Part III. Class 𝒞 and the master induction

**Definition 3.1 (class 𝒞).** A *class-𝒞 world* is (X, Π, c) with X ≥ 2, Π a finite set of primes,
V = V(X, Π) = { s ∈ [2, X) : gcd(s, Π) = 1 }, and caps c : V → ℤ_{≥1} **non-increasing**
(s ≤ s' ⇒ c_s ≥ c_{s'}).

**Lemma 3.2.** Let (X, Π, c) be class 𝒞.
(a) V is divisor-closed.
(b) For every prime q ∉ Π, (V, c) is q-dominated.
(c) (V_{q'}, κ) = (V(X, Π∪{q}), κ) is class 𝒞, i.e. κ is non-increasing.
(d) The real problem: W_n = V(n+1, {p}) with c = ℓ is class 𝒞.

*Proof.* (a) divisors of an integer coprime to Π and < X are coprime to Π and < X.
(b) If u q^i ∈ V then q^i ∈ V (a divisor), and c_{u q^i} ≤ c_{q^i} as u q^i ≥ q^i; sum with weights i.
(c) For q-free u < u': the chain of u has at least as many levels (u q^i < u' q^i) and
c_{u q^i} ≥ c_{u' q^i}; sum over i.
(d) ℓ_r = ⌊log_p(n/r)⌋ + 1 ≥ 1 is non-increasing in r. ∎

**Lemma 3.3 (layers).** Let V be finite with caps c and MC(V, c); let x ∉ V, c_x ≥ 1, V⁺ = V ∪ {x}.
Suppose
  (L) for every M, J_M = { j ∈ [0, c_x] : M / x^j ∈ S(V) } is an interval; and
  (B) whenever N, N x ∈ S(V) there are Q ∈ R_V(N), X ∈ R_V(Nx) such that, writing X − Q = D⁺ − D⁻
      (D^± ≥ 0 disjointly supported), each of D⁺, D⁻ has at most one coordinate ≥ 2.
Then MC(V⁺, c).

*Proof.* A rep of M over V⁺ is Y = Y' + j[x] with Y' ∈ R_V(M/x^j). Layer j (fixed j) is M-connected:
it is a translate of R_V(M/x^j), connected by MC(V). For consecutive nonempty layers j, j+1 apply (B) to
N = M/x^{j+1}: Y1 = X + j[x] and Y2 = Q + (j+1)[x] satisfy Y2 − Y1 = D⁻ − D⁺ + [x], so Y1, Y2 are
M-adjacent. By (L) the nonempty layers are consecutive. ∎

**Definition 3.4.** For a class-𝒞 world, write x := min{ s ≥ X : gcd(s,Π) = 1 } ("the next element").
Then V(X,Π) ∪ {x} = V(x+1, Π). Statement **L(V, x)**: for all M, t ≥ 2:
M, M x^t ∈ S(V) ⇒ M x ∈ S(V). (Iterating, L(V,x) implies (L) of Lemma 3.3 for any c_x.)
Statement **B(V, x)**: (B) of Lemma 3.3.

**Lemma 3.5 (x prime).** If x is prime, L(V, x) and B(V, x) hold.

*Proof.* No element of V (all < x) is divisible by x, so every M ∈ S(V) has v_x(M) = 0; hence M and M x
are never both in S(V), and J_M has at most one element. ∎

**Lemma 3.6 (x a prime power).** Let x = q^k, k ≥ 2, q ∉ Π. If MC holds for (V(X, Π∪{q}), κ), then L(V, x).

*Proof.* By Lemma 3.2(b),(c) and Theorem 2.5, the q-fiber { e : M' q^e ∈ S(V) } is an interval for every
q-free M'. If M, M q^{kt} ∈ S(V) then both exponents v_q(M) and v_q(M)+kt lie in that interval (for
M' = q-free part of M), hence so does v_q(M)+k, i.e. M x ∈ S(V). ∎

**Lemma 3.7.** |V(X, Π∪{q})| < |V(X, Π)| whenever q ∉ Π and q < X.

*Proof.* The left side is a subset of the right side missing q. ∎

**Theorem 3.8 (master induction).** Suppose that for every class-𝒞 world (X, Π, c) whose next element x
is composite **and not a prime power**, L(V(X,Π), x) holds; and that for every class-𝒞 world with
composite next element x, B(V(X,Π), x) holds. Then MC holds for every class-𝒞 world.
Moreover, in proving L(V,x) and B(V,x) one may assume MC for every class-𝒞 world with fewer
elements than V ∪ {x}, hence (Theorem 2.5) that all q-fibers of S(V) are intervals for all primes q ∉ Π.

*Proof.* Induction on |V|. |V| = 0: only the empty rep. Step: let x = max V; V ∖ {x} = V(x, Π) with
restricted (non-increasing) caps, fewer elements, so MC by induction. L(V∖{x}, x) holds by Lemma 3.5
(x prime), Lemma 3.6 + Lemma 3.7 + induction (x a prime power), or hypothesis (otherwise);
B by Lemma 3.5 or hypothesis. Lemma 3.3 gives MC(V). The "moreover" is the induction hypothesis. ∎

**Theorem 3.9 (reduction of the conjecture).** The conjecture follows from:
  **(L\*)** L(V, x) for class-𝒞 worlds whose next element x has at least two distinct prime factors;
  **(B)**  B(V, x) for class-𝒞 worlds whose next element x is composite;
where both may be proved assuming MC (and hence G\* along every prime ∉ Π) for all smaller class-𝒞 worlds.

*Proof.* Theorem 3.8 gives MC(W_n) (Lemma 3.2(d)); then Theorem 1.9. ∎

Compared with HANDOFF §5–6: (i) the setting is now the self-similar class 𝒞 (the recursion into q-free
worlds stays inside it); (ii) Lemma L for prime powers is no longer open; (iii) the induction hypothesis
available when proving (L\*)/(B) is much stronger (fiber-intervals along every prime).

---

## Part III-b. Minimal pairs for (B): proved constraints

Fix a class-𝒞 world V = V(x, Π) (all of [2,x) coprime to Π; x composite, coprime to Π), caps c ≥ 1, and
N with N, Nx ∈ S(V). Choose (Q, X) ∈ R(N) × R(Nx) minimizing |X − Q|_1 and write D = X − Q = D⁺ − D⁻.
Then ∏D⁺ = x · ∏D⁻ (products with multiplicity). "Copies" below means elements of D^± counted with
multiplicity.

**Lemma 3b.1 (closure).** (a) If y, y' are two distinct copies in D⁺ and yy' < x, then X_{yy'} = c_{yy'} and
Q_{yy'} = 0 (so yy' ∈ D⁺). (b) Same for D⁻ with the roles of Q and X swapped.

*Proof.* (a) yy' is coprime to Π and < x, so yy' ∈ V. If X_{yy'} < c_{yy'}, then X' = X − [y] − [y'] + [yy'] is a
rep of Nx (same product) and |X' − Q| ≤ |X − Q| − 1: the two removals each reduce a positive coordinate of
D, the addition changes one coordinate by 1. If Q_{yy'} ≥ 1, then Q' = Q − [yy'] + [y] + [y'] is a rep of N
(room for y, y' in Q because D_y, D_{y'} > 0, and D_y ≥ 2 if y = y'), and |X − Q'| < |X − Q| likewise.
Either contradicts minimality. (b) Symmetric. ∎

**Corollary 3b.2.** If D⁺ has ≥ 2 copies and y_max is a largest one, then y · y_max ≥ x for every other copy y.
Same for D⁻.

*Proof.* Otherwise y y_max ∈ D⁺ by 3b.1, but y y_max > y_max. ∎

**Lemma 3b.3 (quotients).** Let z be a copy in D⁻ and y a copy in D⁺ with z | y, w = y/z ≠ z. Then
X_w = c_w and Q_w = 0 (so w ∈ D⁺). Symmetrically, if y ∈ D⁺ divides z ∈ D⁻ and w = z/y ≠ y, then
Q_w = c_w and X_w = 0.

*Proof.* w ∈ V (a divisor of y), w ≥ 2 since y ≠ z. If X_w < c_w: X' = X − [y] + [z] + [w] is a rep of Nx
(room for z since X_z < Q_z ≤ c_z) and is strictly closer. If Q_w ≥ 1: Q' = Q − [z] − [w] + [y] is a rep of N
(room for y since Q_y < X_y) and strictly closer. The symmetric statement is identical. ∎

**Proposition 3b.4.** If D⁻ = ∅ then D⁺ = {d, x/d} for a factorization x = d·(x/d); in particular D is
M-adjacent and (B) holds for N.

*Proof.* Now ∏D⁺ = x with all elements < x, so D⁺ has k ≥ 2 copies. If k ≥ 3, the smallest copy y and a
largest copy y_max satisfy y · y_max ≤ x / (product of the other ≥ 1 copies) < x, contradicting 3b.2. ∎

---

## Part IV. What is still open (honest status)

* **(L\*)**: Lemma L for next elements x with ≥ 2 distinct prime factors (e.g. x = ab).
  Evidence: no counterexample in any test (HANDOFF §6; this session's profile scan x ≤ 15, n ≤ 400, all p:
  ~1.39M Lemma-L instances, 0 failures).
* **(B)**: the bridge lemma, all composite x.
  Evidence: HANDOFF §6; profile scan (x ≤ 15, n ≤ 400): ~2.49M bridge instances, 0 failures.
  Stronger form suggested by data: **every minimum-distance pair (Q, X) is M-adjacent**; in fact
  (|D⁻|, |D⁺|) ∈ {(0,2), (1,2), (1,3)} in all 1,026,838 tested instances (x ≤ 16, n ≤ 150, all p).
  Part III-b proves the (0, ·) case. Open: rule out |D⁻| ≥ 1 with non-M-adjacent D using 3b.1–3b.3 and
  further local moves.
* Alternative single target (implies MC directly, no layers): **geodesic property** — for reps e ≠ f of N
  that are not M-adjacent, some M-neighbour of e (or of f) is strictly closer in ℓ¹. Holds for every pair
  in the core world for n ≤ 22 (≈ 2.4M pairs at n = 21–22).

---

## Part V. Strengthenings that are FALSE (do not build on them)

All counterexamples are in the real setting (framework B: W = p-free numbers < x, caps ℓ_s from n), and
were found only for n well beyond the n ≤ 24 range of earlier tests. Lesson: **test small x with large n**
(many cap profiles), not only small n.

1. **"greedy(Nx) − greedy(N) is M-adjacent"** (greedy = lex-max count vector, small elements first).
   Holds for n ≤ 16 and even for random element orders, but fails at n = 50, p = 5, x = 18, N = 832:
   greedy(832) = {2³, 8, 13}, greedy(832·18) = {2³, 3², 4², 13}; difference +2[3] +2[4] −[8].
   (A bridge still exists: Q + [3] + [6].)
2. **"The greedy rep Q of N always has an M-adjacent rep of Nx"**: fails at n = 42, p = 3, x = 16,
   N = 40140800, Q = {2³, 4³, 5², 7², 8²}: the unique rep of 16N is {2³,4³,8²,10²,14²}, at difference
   +2[10] +2[14] −2[5] −2[7]. (A bridge exists from Q' = {2³,4²,8²,10,14,5,7}.)
3. **"For Lemma-L instances, the greedy rep admits a simple insertion"** (attach factors of x to hosts
   already in Q): true for all 516,729 instances with n ≤ 24, false at n = 242, p = 11, x = 15,
   N = 2939328, Q = {2³, 3², 6², 9², 14}; the needed move merges two 2's into a host:
   Q − 2[2] + [12] + [5].
4. HANDOFF §8 dead ends remain dead.
