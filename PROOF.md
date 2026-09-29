# PROOF.md — rigorous progress on OEIS A060957 (Yan Sheng Ang's conjecture)

Running file. Everything in Parts I–III is proved in full. Part IV states **exactly** what is still
open, and Part V records strengthenings that are **false** (with explicit counterexamples) so nobody
builds on them. Evidence numbers refer to scripts in `scripts/session2/`.

Status line (update on every commit): **conjecture NOT yet proved.** The whole conjecture is now
reduced (rigorously) to two statements, (L\*) and (B), about "class 𝒞" worlds (Part III, Theorem 3.9).
Proved inside the induction: Lemma L for prime powers x = q^k (Lemma 3.6); the *prime bridge*
(Prop. 3c.3); both (L) and (B) for x = a·b when all primes below a lie in Π (Cor. 3c.4, e.g. x = 2b);
and, for x = ab, M-adjacency of minimum pairs with |D⁻| ≤ 1 (Lemma 3c.6).
Open: (L\*) and (B) for general x with ≥ 2 distinct primes; (B) for prime powers.

**New in Part VI (cap-free route):** a *single-catalyst lemma* (6.1) shows that capacities can never block a
move that needs exactly one spare element. Consequently the conjecture follows from a statement about
multiplicative relations that does **not mention caps at all**: (MC-cat) (Thm 6.3) or, more directly,
(p-cat) about pairs of subsets of [2, n] (Thm 6.5). Both are open but hold in every test (Part VI.4), and
(p-cat) already forces a rigid chain structure on any counterexample (Lemma 6.6, proved).

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

## Part III-c. Prime bridges, and the case x = q·b with q the smallest available prime

Throughout this part V is divisor-closed with caps c, q a prime, (V, c) q-dominated, and we use the
q-decomposition of Part II (core vectors m over (V_{q'}, κ), I(m) = [lo(m), hi(m) + T_q]).
A **single move** from a rep Y is a rep Y' with Y' − Y having at most one entry +1, at most one entry −1,
and all other entries 0.

**Lemma 3c.1 (single up-move).** Let Y be a rep of M q^e whose core vector is m, and suppose
e < hi(m) + T_q. Then there is a rep Y' of M q^{e+1} with the same core vector m such that Y' − Y is a
single move.

*Proof.* The q-exponent of Y is the sum of the level sums of the chains plus the pure-chain sum. Since the
total is below hi(m) + T_q, some chain u has level sum < hi_u(m_u), or the pure part has sum < T_q.
In the first case the proof of Lemma 2.1 gives a copy at a level i with a free copy at level i+1; moving it
is the single move −[u q^i] + [u q^{i+1}]. In the second case: if the pure level 1 (block q) has room, add
it (+[q]); otherwise let j ≥ 2 be the least level with a free copy (it exists, the pure part not being full);
level j−1 is full, hence used, and −[q^{j−1}] + [q^j] is a single move. Each case raises the exponent by 1
and keeps the core vector. ∎

**Lemma 3c.2 (crossing).** Let I_0, …, I_s be integer intervals with I_{i} ∩ I_{i+1} ≠ ∅ for all i,
α ∈ I_0 and α + 1 ∈ I_s. Then some I_i contains both α and α + 1.

*Proof.* Let i* be the largest index with α ∈ I_{i*}. If α + 1 ∈ I_{i*} we are done; otherwise
max I_{i*} = α, so i* < s. For j > i*, α ∉ I_j; by induction each I_j ⊆ (−∞, α−1]: I_{i*+1} meets
I_{i*} ⊆ (−∞, α] and misses α, and each later I_j meets I_{j−1} ⊆ (−∞, α−1] and misses α. This
contradicts α + 1 ∈ I_s. ∎

**Proposition 3c.3 (prime bridge, PB).** Assume MC holds for (V_{q'}, κ) (at least for the product
M = N_{q'}). If N, N q ∈ S(V), then there are Q ∈ R(N) and X ∈ R(Nq) with X − Q a single move
(in particular M-adjacent).

*Proof.* Let α = v_q(N). By Lemma 2.2 there are core vectors m, m' of M with α ∈ I(m), α+1 ∈ I(m').
By MC(V_{q'}) they are joined by an M-path, along which consecutive intervals intersect (proof of
Theorem 2.5). By Lemma 3c.2 some core vector μ on the path has α, α+1 ∈ I(μ). Take any rep Q of N
with core vector μ (Lemma 2.2) and apply Lemma 3c.1. ∎

**Corollary 3c.4 (x = q·b, q the smallest prime outside Π).** Let (x, Π, c) be class 𝒞 with
V = V(x, Π), x = a·b with a < b primes, and suppose every prime < a lies in Π. Assume MC for all
class-𝒞 worlds with fewer elements than V ∪ {x}. Then L(V, x) and B(V, x) hold.

*Proof.* Every integer in [2, a) has a prime factor < a, so V ∩ [2, a) = ∅. If b·w ∈ V then w < a, so
w = 1: **b is the only element of V divisible by b.** Hence V' := V ∖ {b} is divisor-closed, and for b-free
M, M b^j ∈ S(V) ⇔ (M ∈ S(V') and j ≤ c_b), reps of b-free products being the same over V and V'.
Write N = N' b^β with b ∤ N'.
(L) If N (ab)^t ∈ S(V) then N' a^t ∈ S(V') and β + t ≤ c_b. For b-free M the a-fiber of M in S(V') equals
its a-fiber in S(V), an interval by Theorem 2.5 applied to V (MC(V(x, Π∪{a})) holds by hypothesis;
domination by Lemma 3.2). So N' a ∈ S(V'), and β + 1 ≤ c_b; thus N ab = N' a b^{β+1} ∈ S(V).
(B) If N, Nab ∈ S(V) then N', N'a ∈ S(V') and β + 1 ≤ c_b. V' is a-dominated (its pure a-chain and a-chains
are those of V, minus the one-element chain {b}), and its a-free core vectors of the b-free product
N'_{a'} are exactly those over V_{a'}, which are M-connected by hypothesis. Proposition 3c.3 in V' gives
Q' ∈ R_{V'}(N'), X' ∈ R_{V'}(N'a) differing by a single move. Then Q = Q' + β[b] ∈ R(N),
X = X' + (β+1)[b] ∈ R(Nab), and X − Q = (X' − Q') + [b] has entries in {−1, 0, 1}: M-adjacent. ∎

In the real problem (Π = {p}) this settles every x = 2b (p odd) and x = 3b (p = 2); inside the class-𝒞
recursion it settles x = q_0 b for the least prime q_0 ∉ Π.

**Lemma 3c.5 (composition).** If Y − Q and X − Y are single moves then X − Q is M-adjacent.

*Proof.* X − Q is a sum of two vectors each with at most one +1 and one −1; an entry +2 needs both +1's
at the same place and an entry −2 needs both −1's at the same place. ∎

**Lemma 3c.6 (semiprime minimal pairs with |D⁻| ≤ 1).** In the setting of Part III-b, let x = ab with a ≠ b
primes, and let (Q, X) be a minimum-distance pair with |D⁻| ≤ 1 (counted with multiplicity). Then D is
M-adjacent; in fact all entries of D are in {−1, 0, 1}.

*Proof.* If D⁻ = ∅ use Proposition 3b.4. Let D⁻ = {z} (one copy); then ∏D⁺ = a·b·z. No element of V
is divisible by ab (it would force ab ∈ V by divisor-closedness, but ab = x ∉ V). Fix a bijection between
the prime factors (with multiplicity) of ∏D⁺ and those of a·b·z respecting primes; the copy receiving a,
the copy receiving b are distinct copies y_a ≠ y_b. Every other copy y receives only primes of z, so y | z.
By Lemma 3b.3 (second part), z/y ∈ D⁻ unless z/y = y; since D⁻ = {z} and z/y ≠ z, we get z = y². The
special case y ∈ D⁺, y² = z ∈ D⁻ forces c_y = 1, X_y = 1, Q_y = 0: indeed Q − [y²] + 2[y] (valid if
Q_y ≤ c_y − 2) and X − 2[y] + [y²] (valid if X_y ≥ 2) would both be strictly closer; so Q_y ≥ c_y − 1 and
X_y ≤ 1, while D_y ≥ 1. Hence there is at most one such y (two copies would give D_y ≥ 2), and
D⁺ ⊆ {y_a, y_b, y} consists of pairwise different types each of multiplicity 1 (y_a and y_b differ because
one is divisible by a and not b, the other the reverse; y differs from both since D_y = 1). ∎

Evidence that the remaining case is only a finite local analysis: for semiprime x ∈ {6, 10, 14, 15}, all
n ≤ 100, all p, every pair (Q, X) that cannot be shortened by a single merge (y, y' → yy') or split on Q
or on X is M-adjacent (≈ 3.3M locally minimal pairs; `scripts/session2/locmin.py 15 100 3 … semi`);
with 4-block moves allowed, locally minimal pairs even have |D⁻| ≤ 1 (≈ 3.0M pairs).

---

## Part IV. What is still open (honest status)

* **(L\*)**: Lemma L for next elements x with ≥ 2 distinct prime factors (e.g. x = ab), except the case
  covered by Corollary 3c.4. Evidence: no counterexample in any test (HANDOFF §6; this session's profile
  scan x ≤ 15, n ≤ 400, all p: ~1.39M Lemma-L instances, 0 failures).
  Where it breaks: via the a-decomposition, (L\*) for x = ab would follow if max{hi_a(m)} over core vectors
  of N_{a'} b^j were concave in j (and the min convex); for a fixed {a,b}-free core vector this holds (it is
  a resource allocation), but the maximum over core vectors of concave functions need not be concave.
* **Route (Lip) for (L\*)**, x = a^k b^l with a, b distinct primes (k, l ≥ 1). Fix an {a,b}-free K and put
  F = { (i, j) : K a^i b^j ∈ S(V) }, rows R_j = { i : (i, j) ∈ F }.
  *Lemma IV.1 (proved).* Rows are intervals [A(j), B(j)] and the nonempty rows form an interval of j's (G\* along
  a in V; and R_j ≠ ∅ ⇔ K b^j ∈ S(V_{a'}, κ) by Lemma 2.2, an interval in j by G\* along b in the class-𝒞 world
  V(x, Π∪{a}), all available inside the master induction). If moreover **(Lip_x)** A(j+l) ≤ A(j) + k and
  B(j+l) ≤ B(j) + k whenever R_j, R_{j+l} ≠ ∅, then L(V, x) holds for this K.
  *Proof.* Let (i, j), (i + Tk, j + Tl) ∈ F, T ≥ 2. Rows j + l, …, j + Tl are nonempty. A(j+l) ≤ A(j) + k ≤ i + k,
  and B(j+Tl) ≤ B(j+l) + (T−1)k gives B(j+l) ≥ i + Tk − (T−1)k = i + k. So (i+k, j+l) ∈ F. ∎
  (Same with the roles of a and b exchanged — "columns".) By complement duality (e ↦ c − e maps F_K to a point
  reflection of F_{K'}), the A-half and the B-half of (Lip_x) are equivalent over all K.
  Evidence (`lipv.py`, n ≤ 200, all p): semiprimes x ≤ 22: the row version with b = the larger prime always
  holds, the column version fails at x = 21; x = 12, 20 (= a²b): rows hold, columns fail; x = 18 (= a b²):
  columns hold, rows fail. In every tested (x, K) at least one orientation holds. Open: a proof of (Lip_x).
  For x = ab (a < b), within one {a,b}-free core vector the rows do satisfy it (every b-block is ub with u < a,
  and it only takes a block away from the a-chain of u, so the per-core maximum B_μ(j) is non-increasing in j
  on its feasible range); the difficulty is again the union over cores.
* **Two-step route for (B)** (evidence, x ∈ {6,10,12,14,15}, n ≤ 150, 525,172 instances, 0 failures):
  some intermediate N·q (q | x) is representable, and there is Y ∈ R(Nq) with single moves Q → Y → X.
  By Lemma 3c.5 this would give (B). Existence of such Y is open.
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
5. **"3-local minimality ⇒ M-adjacency" (for bridges)** — i.e. a pair (Q, X) that cannot be shortened by one
   merge y·y' or one split, on either side, is M-adjacent. True for all semiprime x ≤ 15, n ≤ 100, but false at
   x = 14, p = 5, n = 150: D = X − Q = +[7] + 2[8] + 2[9] − 3[6] − [12]. It is shortened only by the 2↔2 swap
   8·9 = 6·12 (a ratio-1 part of D; see Part VI, where such parts are always usable).
6. **(Lip) in general class-𝒞 worlds.** For primes a ≠ b and a fixed {a,b}-free part, let [A(j), B(j)] be the
   set of a-exponents with b-exponent j. "A(j+1) ≤ A(j)+1 and B(j+1) ≤ B(j)+1" fails in general worlds
   (V = 5-free numbers < 13 with a = 2, b = 3: 1532 failures; X = 18: 33,479 of 33.3M steps). It also fails
   in the Lemma-L worlds V(x, Π) for x = 18 = 2·3² and x = 24 = 2³·3 in the orientation needed below
   (Part IV, route (Lip)).

---

## Part VI. Catalysts: a cap-free route

Notation. V is a finite set of integers ≥ 2. For D ∈ ℤ^V let D⁺, D⁻ be its positive and negative parts,
|D| = Σ|D_v|, and ρ(D) = ∏ v^{D_v} ∈ ℚ_{>0} (the *ratio*). D is a *relation* if ρ(D) = 1.
A *part* of D is a vector E with E_v between 0 and D_v for every v; then D − E is also a part and
ρ(D) = ρ(E) ρ(D − E). Reps and caps are as in Part II, with all caps ≥ 1.

**Lemma 6.1 (single catalyst).** Let 0 ≤ e ≤ c and 0 ≤ e + D ≤ c. Let E be a part of D, z ∈ V with D_z = 0,
and s ∈ {+1, −1}. Then at least one of g₁ = e + E − s[z], g₂ = e + (D − E) + s[z] satisfies 0 ≤ g ≤ c.
Both have g_v between e_v and (e + D)_v for all v ≠ z, and ∏g₁ = ∏e · ρ(E) z^{−s}, ∏g₂ = ∏e · ρ(D − E) z^{s}.

*Proof.* For v ≠ z the entries E_v, (D − E)_v lie between 0 and D_v. At z the two candidates are e_z − s and
e_z + s; since 0 ≤ e_z ≤ c_z and c_z ≥ 1, one of them lies in [0, c_z]. ∎

So a move that needs one spare element z ∉ supp(D) is never blocked by capacities: it can always be made
from one of the two ends. (Moves needing two spare elements can be blocked.)

**Definition 6.2.** (MC-cat)(V): every relation D ≠ 0 on V that is **not** M-adjacent has a part
E ∉ {0, D} with ρ(E) = 1 or ρ(E) = z^{±1} for some z ∈ V with D_z = 0.

**Theorem 6.3.** If (MC-cat)(V) holds, then for **every** cap vector c ≥ 1 on V and every M, the reps of M are
M-connected.

*Proof.* Let e, f be reps of M, D = f − e (a relation). Induct on |D|. If D is M-adjacent we are done.
Otherwise take E from (MC-cat). If ρ(E) = 1, then g = e + E is a rep of M (coordinatewise between e and f)
with |g − e| = |E| < |D| and |f − g| = |D − E| < |D|; apply induction to (e, g) and (g, f).
If ρ(E) = z^{s}, note |E| ≥ 2: otherwise E = ±[v] with D_v ≠ 0, and ρ(E) = v^{±1} = z^{±1} would force v = z,
but D_z = 0. Likewise ρ(D − E) = z^{−s} gives |D − E| ≥ 2. By Lemma 6.1 one of g₁ = e + E − s[z],
g₂ = e + (D − E) + s[z] is a rep (both have product M). Their distances to e and to f are |E| + 1 and
|D − E| + 1 (in some order), both < |D|. Apply induction. ∎

**Corollary 6.4.** If (MC-cat)(W_n) holds (W_n = p-free numbers in [2, n]), the conjecture holds for (n, p)
(Theorem 6.3 with c = ℓ, then Theorem 1.9). No induction over worlds, no (L\*)/(B), no monotonicity of caps.

The same lemma applies to the layer lemmas: a minimum-distance pair (Q, X) for (B) has no split
D = E + (D − E) with ρ(D − E) ∈ {1} ∪ {z^{±1} : z ∈ V, D_z = 0}, D − E ≠ 0 (if ρ(D − E) = z^{s}, then
ρ(E) = x z^{−s}, and by Lemma 6.1 one of the pairs (Q, Q + E + s[z]) — products N, Nx — and
(Q + (D − E) − s[z], X) — products N, Nx — is valid; both have length |E| + 1 < |D|). So (B) for **all caps**
follows from the cap-free statement **(B-cat)**: every relation of ratio x on V(x, Π) without such a split
is M-adjacent.

**Theorem 6.5 (direct form).** Fix n and p ≤ n. Suppose **(p-cat)**: for all disjoint D⁺, D⁻ ⊆ [2, n] with
∏D⁺ = p^t ∏D⁻ and t ≥ 2, there are A ⊆ D⁺, B ⊆ D⁻ (possibly empty or everything) and 0 < k < t with
  ∏A = p^k ∏B,  or  ∏A = p^k w ∏B,  or  w ∏A = p^k ∏B,
for some w ∈ [2, n] ∖ (D⁺ ∪ D⁻) (a *certificate*). Then the conjecture holds for (n, p).

*Proof.* Show by strong induction on t: if m, m p^t ∈ P_n then m p^k ∈ P_n for 0 ≤ k ≤ t. For t ≤ 1 there is
nothing to prove. Let S, T ⊆ [2, n] with ∏S = m, ∏T = m p^t (the element 1 never matters), D⁺ = T ∖ S,
D⁻ = S ∖ T. Take a certificate. If ∏A = p^k ∏B, then U = (S ∖ B) ∪ A has product m p^k.
If ∏A = p^k w^{s} ∏B (s = ±1, w ∉ D⁺ ∪ D⁻, so w ∈ S ⇔ w ∈ T): U₁ = (S ∖ B) ∪ A has product m p^k w^s and
U₂ = (T ∖ A) ∪ B has product m p^{t−k} w^{−s}. If s = 1 and w ∈ S, U₁ ∖ {w} has product m p^k; if s = 1 and
w ∉ S (so w ∉ T), U₂ ∪ {w} has product m p^{t−k}. The case s = −1 is symmetric. In all cases m p^{k'} ∈ P_n
for some 0 < k' < t; apply the induction hypothesis to (m, k') and (m p^{k'}, t − k'). ∎

**Lemma 6.6 (structure of a certificate-free pair).** Let (D⁺, D⁻) be as in (p-cat) with no certificate,
L = ⌊log_p n⌋, and C_r = { r p^i ≤ n } (levels 0, …, ℓ_r − 1) for p-free r. Then
 (i) p, p², …, p^L ∈ D⁻, and D⁺ contains no power of p;
 (ii) for every p-free r ≥ 2 there are 0 ≤ α_r ≤ β_r ≤ ℓ_r with D⁺ ∩ C_r = levels [0, α_r) and
      D⁻ ∩ C_r = levels [β_r, ℓ_r);
 (iii) t = Σ_r C(α_r, 2) − L(L+1)/2 − Σ_r Σ_{j=β_r}^{ℓ_r−1} j, and ∏_r r^{α_r} = ∏_r r^{ℓ_r − β_r}.

*Proof.* Write F = [2, n] ∖ (D⁺ ∪ D⁻).
(a) If p^j ∈ F for some 1 ≤ j < t, then A = B = ∅, w = p^j is a certificate (w·1 = p^j·1). Since t ≥ 2 and
p ≤ n, this gives p ∈ D⁺ ∪ D⁻. If p ∈ D⁺, A = {p}, B = ∅ is a certificate (k = 1). So p ∈ D⁻.
(b) Let y = r p^i ∈ D⁺ with i ≥ 1 and y ≠ p, and y' = r p^{i−1} (≥ 2). If y' ∈ F, A = {y}, B = ∅, w = y' is a
certificate (∏A = p w); if y' ∈ D⁻, A = {y}, B = {y'} is one (∏A = p ∏B). Hence y' ∈ D⁺. So D⁺ ∩ C_r is
closed downwards; for r = 1 this would reach p ∈ D⁺, impossible, so D⁺ has no power of p.
(c) Let z = r p^j ∈ D⁻ and z' = r p^{j+1} ≤ n. If z' ∈ F, A = ∅, B = {z}, w = z' is a certificate
(w = p ∏B); if z' ∈ D⁺, A = {z'}, B = {z} is one. Hence z' ∈ D⁻: D⁻ ∩ C_r is closed upwards. With (a),
all of p, …, p^L lie in D⁻.
(ii) follows from (b), (c) and disjointness; (iii) is the p-adic and p-free part of ∏D⁺ = p^t ∏D⁻. ∎

So in a hypothetical counterexample D⁺ consists of *bottom* segments of chains and D⁻ of the whole pure chain
plus *top* segments.

### VI.3 A minimal counterexample, sub-balances, and the "heavy step" reduction

**Setting M.** Suppose the conjecture fails for (n, p). Then there are m and t ≥ 2 with m, m p^t ∈ P_n and
m p^k ∉ P_n for 0 < k < t (take two consecutive members of E_n(R) around a gap). Among all S, T ⊆ [2, n]
with ∏S = m, ∏T = m p^t choose one with |S Δ T| minimal, and put D⁺ = T ∖ S, D⁻ = S ∖ T, F = [2,n] ∖ (S Δ T).
Then there is no pair A ⊆ D⁺, B ⊆ D⁻ with
 (1) ∏A = p^k w^ε ∏B, 0 < k < t, ε ∈ {0, ±1}, w ∈ F (a (p-cat) certificate: gives m p^{k'} ∈ P_n, 0<k'<t);
 (2) (A, B) ∉ {(∅, ∅), (D⁺, D⁻)} and ∏A = ∏B or ∏A = p^t ∏B ((S ∖ B) ∪ A would give a pair closer than
     (S, T) with the same two products);
 (3) (A, B) ∉ {(∅, ∅), (D⁺, D⁻)} and ∏A = w^{±1} ∏B or ∏A = p^t w^{±1} ∏B with w ∈ F (Lemma 6.1 with all
     caps 1 gives a strictly closer pair, as in the proof of Theorem 6.3).
In particular Lemma 6.6 applies. Keep its notation, put m_r = ℓ_r − β_r and T0 = L(L+1)/2.

**Definition.** A *sub-balance* is σ = (c⁺, c⁻) with 0 ≤ c⁺_r ≤ α_r, 0 ≤ c⁻_r ≤ m_r (r ≥ 2 p-free) and
∏_r r^{c⁺_r} = ∏_r r^{c⁻_r}. A *realization* of σ is a pair (A, B): A consists of c⁺_r elements of D⁺ ∩ C_r
for each r, B of c⁻_r elements of D⁻ ∩ C_r for each r ≥ 2 together with an arbitrary subset of {p, …, p^L}.
Write σ ≤ σ' for the componentwise order; 0 and σ_full = (α, m) are the extreme sub-balances.

**Lemma 6.7 (realizable exponents form an interval).** Every realization of σ has ∏A = p^δ ∏B, and the set of
these δ is the integer interval I(σ) = [lo(σ) − T0, hi(σ)], where
 hi(σ) = Σ_r [c⁺_r(α_r − 1) − C(c⁺_r, 2)] − Σ_r [c⁻_r β_r + C(c⁻_r, 2)],
 lo(σ) = Σ_r C(c⁺_r, 2) − Σ_r [c⁻_r(ℓ_r − 1) − C(c⁻_r, 2)].
*Proof.* The p-free parts cancel by definition. Per chain, the level sums of c-element subsets of a segment of
consecutive levels form an interval (Lemma 1.2, shifted); the pure part contributes −[0, T0] (Lemma 1.3); a sum
of integer intervals is an integer interval. The endpoints are the stated extreme choices. ∎

**Lemma 6.8 (dichotomy).** In Setting M, I(0) = [−T0, 0], I(σ_full) = [t, t + T0], and for every other
sub-balance σ either I(σ) ⊆ (−∞, −1] ("low") or I(σ) ⊆ [t + 1, ∞) ("high").
*Proof.* For σ = σ_full all non-pure elements are used and B ⊇ … varies over subsets of the pure chain, so
δ = t + T0 − (subset sum). For σ ∉ {0, σ_full} a realization with δ ∈ [0, t] would be a forbidden pair of type
(1) or (2): it is not (∅, ∅) (σ ≠ 0 uses a non-pure element) and not (D⁺, D⁻) (σ ≠ σ_full misses one). ∎

**Lemma 6.9 (one step up).** If σ ≤ σ' and d_r = c'⁺_r − c⁺_r, then lo(σ') − hi(σ) ≤ Σ_r C(d_r, 2).
*Proof.* Per chain in D⁺: C(c+d, 2) − [c(α−1) − C(c, 2)] = c(c + d − α) + C(d, 2) ≤ C(d, 2) as c + d ≤ α. Per
chain in D⁻ the contribution is BOT(c⁻) − TOP(c'⁻) ≤ 0 (the lowest c⁻ levels of a segment sum to at most its
highest c'⁻ ≥ c⁻ levels). ∎

**Proposition 6.10 (a heavy step is unavoidable).** In Setting M, along every chain of sub-balances
0 = σ_0 < σ_1 < … < σ_K = σ_full some step has Σ_r C(c⁺_r(σ_{i+1}) − c⁺_r(σ_i), 2) ≥ T0 + t.
*Proof.* Let i + 1 be the least index with I(σ_{i+1}) ⊆ [t, ∞) (i + 1 = K at the latest). By Lemma 6.8,
I(σ_i) ⊆ (−∞, 0], i.e. hi(σ_i) ≤ 0, while lo(σ_{i+1}) − T0 ≥ t. Now apply Lemma 6.9. ∎

Since C(d_r, 2) ≤ C(ℓ_r, 2) ≤ T0 (Lemma 1.6), a heavy step must raise at least two D⁺-chains by ≥ 2 each.
Hence:

**Corollary 6.11 (reduction).** The conjecture holds for (n, p) if in every configuration of Setting M the
p-free balance admits a chain of sub-balances from 0 to σ_full whose steps are all *light*
(Σ_r C(d_r, 2) < T0 + t) — e.g. if it decomposes into sub-balance increments each of which raises at most one
D⁺-chain by more than 1.

**Lemma 6.12 (products stay in D⁺).** In Setting M, let r, r' be p-free with rr' ≤ n. If r ≠ r' and
α_r, α_{r'} ≥ 1, then α_{rr'} ≥ min(ℓ_{rr'}, α_r + α_{r'} − 1). If r = r' and α_r ≥ 2, then
α_{r²} ≥ min(ℓ_{r²}, 2α_r − 2) and α_{r²} ≥ 1.
*Proof.* Let g = α_{rr'}; if g = ℓ_{rr'} there is nothing to prove. Otherwise v = rr' p^g is in F or in D⁻.
For A = {r p^i, r' p^{i'}} (i < α_r, i' < α_{r'}, i ≠ i' if r = r') we get ∏A = p^{e} v ∏∅ (v ∈ F) or
∏A = p^{e} ∏{v} (v ∈ D⁻) with e = i + i' − g. The realizable e form the interval [−g, α_r + α_{r'} − 2 − g]
(resp. [1 − g, 2α_r − 3 − g]), whose left end is ≤ 1 ≤ t − 1. If its right end were ≥ 0, some choice would
give e ∈ [0, t]: a forbidden pair of type (1), (2) or (3) — note (A, B) ≠ (D⁺, D⁻) because D⁻ contains p
(Lemma 6.6) and B ⊆ {v}. Hence g ≥ α_r + α_{r'} − 1 (resp. g ≥ 2α_r − 2 ≥ 2). ∎

So D⁺ is closed under products ≤ n (with growing bottom segments), while by Proposition 6.10 the balance must
contain a "heavy" primitive relation among the p-free parts, i.e. one using ≥ 2 copies each of at least two
distinct p-free parts of D⁺ with Σ C(d_r, 2) ≥ T0 + 2. **Open:** show that Lemma 6.12 (and the analogous
quotient rules) leave room only for light decompositions. Evidence: `structcfg.py` finds every Lemma-6.6
configuration with t ≥ 2 (n ≤ 50, p ∈ {3, 5, 7}, up to 4·10⁵ configurations each) certificate-bearing.

### VI.4 Evidence for the cap-free statements (all 0 counterexamples)

* (MC-cat): exhaustive over relations with ∏D⁺ ≤ 2·10⁵ on V(X, ∅), X ≤ 17 (75,295 non-M-adjacent
  relations), and ∏D⁺ ≤ 10⁶ for X = 18 (236,828) and X = 20 (466,607); odd worlds V(X, {2}), X ≤ 23.
  Certificates are local: for X = 17 the smallest certificate has size |A| + |B| ≤ 3 in all but 16 cases
  (those use 2↔2 swaps such as 5·9 = 3·15), maximum 5. (`mccat.py`, `catshape.py`)
* (B-cat): ratio-x relations with ∏D⁻ ≤ 3·10⁵, x = X ∈ {6, 10, 12, 14, 15, 18}: 0 catalyst-free non-M-adjacent.
* (p-cat): exhaustive over all disjoint D⁺, D⁻ ⊆ [2, n], n ≤ 12, all p. (`pcat.py`)
* MC itself for **random non-monotone caps** in [1, 3] on V(X, Π) (X ≤ 14, six choices of Π): 449,119
  products, all M-connected; (L\*) never failed either (`mcrand.py`). So monotonicity of caps is not needed,
  consistent with a cap-free proof.

---

## Part VII. Empirical generalizations (not needed, but they suggest the "right" statement)

* **All directions in P_n.** For every n ≤ 22, every m ∈ P_n and every ratio r = y/z with y, z ≤ 24,
  gcd(y, z) = 1, the set { e ∈ ℤ : m r^e ∈ P_n } is an interval (12.6M fibers at n = 22; `pn_mixed.py`).
  For integer ratios y ≤ 150 this holds for n ≤ 26 (32M fibers at n = 26; `pn_ally.py`). I.e. the set of
  exponent vectors of P_n meets every lattice line in consecutive lattice points. (It is **not** the set of
  lattice points of its convex hull — HANDOFF §8 — and abstract divisor-closed vector worlds with arbitrary
  caps do have holes in 3-D, e.g. along (1, −1, 0) and (1, 1, 1): `scripts/random-abstract/dirs.py`.)
* **(L\*) for every y, not just the next element.** In class-𝒞 worlds V = p-free numbers < X (X ≤ 16, caps
  from every n ≤ 120), every y-fiber is an interval for every composite y ≤ 3X coprime to p: y ∈ V, y = next
  element, and y beyond (14.9M fibers; `ylstar.py`).
