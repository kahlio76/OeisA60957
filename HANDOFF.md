# HANDOFF — proving OEIS A060957 (Yan Sheng Ang's conjecture) in Lean

> **STATUS (2026-09-29): PARKED.** Later work is in `PROOF.md` (merged from the session2 branch) and
> `scripts/session2/`. Read `PROOF.md` first: it supersedes §6/§9 below. The conjecture is still NOT proved
> and no Lean work exists. Everything reduces to one missing global counting step (Claim*, PROOF.md VI.6/VI.10).
> The per-level Hall inequality and the Prod+Quot+balance ablation are the newest leads.


Read this whole file before doing anything. It records everything learned in one long
local session (2026-09-28) so a fresh session can continue without redoing work.

---

## 0. TL;DR

* **Goal:** a complete, `sorry`-free Lean 4 proof of `OeisA60957.conjecture`
  (DeepMind `formal-conjectures`, file `FormalConjectures/OEIS/60957.lean`, copied in `lean/`).
  Problems in that repo are sometimes picked up by external Lean-proof venues.
* **Status:**
  * The conjecture holds for **every n ≤ 46** (exhaustive, all primes p, all m).
  * A clean **reduction** is proved on paper (§3–§5).
  * The whole theorem now follows from **two lemmas** (§6). Both hold in every
    exhaustive and random test, but **neither has a hand proof yet**.
  * **No Lean work has started.**
* **The real open part is the math of §6.** Every attempt so far died on the same
  obstacle, "capacity blocking" (§8). The Lean work only starts once there is a paper proof.
* **Honest odds** (from the session's own estimate): well under 50% that the current
  approach closes. Try hard, but also report back honestly.

---

## 1. Exact target statement (Lean)

```lean
namespace OeisA60957
def productsOfSubsets (n : ℕ) : Set ℕ := {m : ℕ | ∃ s ⊆ Finset.Icc 1 n, m = s.prod id}

theorem conjecture (n : ℕ) (p : ℕ) (hp : p.Prime) (hpn : p ≤ n)
    (m a_exp : ℕ) (h1 : m ∈ productsOfSubsets n) (h2 : p ^ a_exp * m ∈ productsOfSubsets n)
    (k : ℕ) (hk1 : 0 < k) (hk2 : k < a_exp) :
    p ^ k * m ∈ productsOfSubsets n
```

* m may itself contain factors of p.
* The claim is equivalent to the statement below. For every p-free integer R, the set
  E_n(R) = { t : R·p^t is a product of a subset of [1..n] }
  is an interval of integers (possibly empty).
* Setting m = R·p^{t0} gives the original from this. Conversely, the original with
  m = R·p^{min E} gives this.

OEIS page (checked 2026-09-28) still lists it as a conjecture (Yan Sheng Ang, Feb 13 2020).
There is no proof and no prior formalization. Before submitting, re-check
github.com/plby/lean-proofs, because a prior external formalization gets rejected
with PRIOR_EXTERNAL_FORMALIZATION.

---

## 2. Lean / submission environment

The local validator-matched environment was at `~/Developer/conjectures-lean` on the
user's Mac. It is NOT in this repo, so rebuild it in the cloud.

* Lean toolchain: `leanprover/lean4:v4.33.1`.
* Mathlib rev `0df444a360eaa60ab8c11dca51a86af692955474`, pulled in via
  formal-conjectures, input rev `v4.33.1`.
* formal-conjectures commit `7d1a8c99…` (the validator pin).
* The local copy also had a "tasks audit patch". It doesn't matter for this file.
* Lake options used by the validator:
  * `warn.sorry = false`
  * `weak.google.answer = "always_true"`

Suggested setup:

```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
git clone https://github.com/google-deepmind/formal-conjectures && cd formal-conjectures
git checkout 7d1a8c99   # if that short hash fails, use the latest commit where 60957.lean matches lean/60957.lean
lake exe cache get      # downloads Mathlib oleans (~10–20 min)
lake build FormalConjectures.OEIS.«60957»
```

Write the proof in a separate file. It must import the statement and prove
`OeisA60957.conjecture` exactly as stated. The file must not contain `sorry`,
`axiom`, or `native_decide` abuse.

Useful Lean facts:
* The file's `a n` tests (`a_0`…`a_5`) are `decide`.
* Direct `decide` on the theorem is impossible, since the statement is for all n.

---

## 3. The reduction (PROVED on paper)

### 3.1 Chains and levels
Fix n and a prime p ≤ n.

* **Chains.** Every x ∈ [2..n] is uniquely x = r·p^j with r p-free. Call r the
  **position** and j the **level**.
  * For p-free r ≥ 2 the chain C_r = {r, rp, rp², …} ∩ [1..n] has length
    ℓ_r = ⌊log_p(n/r)⌋ + 1, with levels 0..ℓ_r−1.
  * ℓ_r is non-increasing in r (numerically, not only by divisibility).
* **Pure chain.** Chain 1 = {p, p², …, p^L} with L = ⌊log_p n⌋. The element 1 is irrelevant.
  * Its subsets contribute any p-exponent in [0, T0], T0 = L(L+1)/2.
  * Every r ≥ 2 has ℓ_r ≤ L, hence C(ℓ_r, 2) ≤ T0.
  * (In the order-ideal language of §3.4 the pure column is written with L_0 − 1 = L.)
* **Representations.** A subset S ⊆ [2..n] with p-free part R determines a
  **representation (rep)**: a count vector e = (e_r)_r with 0 ≤ e_r ≤ ℓ_r and
  ∏ r^{e_r} = R.
* **Interval of a rep.** For a fixed rep e, placing e_r elements on distinct levels of
  C_r in all possible ways gives p-exponents forming exactly the interval
  J(e) = [lo(e), hi(e)], where
  * lo(e) = Σ_r C(e_r, 2) (all copies bottom-packed),
  * hi(e) = Σ_r [C(ℓ_r, 2) − C(ℓ_r − e_r, 2)] (top-packed),
  * hi(e) − lo(e) = Σ_r e_r(ℓ_r − e_r).

  Why it is an interval: move one element up one free level at a time. This is the
  q-binomial support.
* **So:** E_n(R) = ⋃_{reps e of R} ( J(e) + [0, T0] ).

  The conjecture ⇔ this union of intervals is an interval for every p-free R.

### 3.2 Lemma P1 (overlap of two reps) — PROVED
For reps e, f of the same R:

  lo(f) ≤ hi(e) + Σ_{r : f_r > e_r} C(f_r − e_r, 2).

**Proof.**
1. lo(f) − lo(e) = Σ_r [C(f_r,2) − C(e_r,2)].
2. For a_r = f_r − e_r > 0 this term equals a_r e_r + C(a_r, 2). For a_r ≤ 0 it is ≤ 0.
3. Also hi(e) − lo(e) = Σ e_r(ℓ_r − e_r) ≥ Σ_{a_r>0} e_r a_r, because f_r ≤ ℓ_r
   means a_r ≤ ℓ_r − e_r.
4. Combining the two: lo(f) ≤ hi(e) + Σ_{a_r > 0} C(a_r, 2). ∎

With the pure-chain slack, J(e)+[0,T0] and J(f)+[0,T0] overlap or touch as soon as
both conditions hold:

  Σ_{f_r>e_r} C(f_r−e_r, 2) ≤ T0 + 1   and   Σ_{e_r>f_r} C(e_r−f_r, 2) ≤ T0 + 1.

### 3.3 M-moves (the key notion)
**Definition.** e and f are **M-adjacent** if
* at most one coordinate has f_r − e_r ≥ 2, and
* at most one coordinate has f_r − e_r ≤ −2.

All other coordinates differ by at most 1.

Since C(ℓ_r, 2) ≤ T0, P1 implies that M-adjacent reps have overlapping or touching
intervals.

**Consequence.** If the reps of each class R are connected under M-moves, the conjecture
follows. This is **M-connectivity**. It needs no level bookkeeping at all: the M-relation
does not even depend on the caps.

### 3.4 Order-ideal language (equivalent, cleaner)
* Let D ⊂ ℕ^d∖{0} be the set of prime-exponent vectors of 2..n. D is a
  **finite order ideal** (down-closed): divisors of numbers ≤ n are ≤ n.
* The conjecture says the subset sums of D are hole-free along the coordinate e_p.
* Write each vector as (height, position):
  * height = the p-coordinate,
  * position = the remaining coordinates, i.e. the p-free part.
* Columns have lengths L_x, which are monotone:
  x ≤ x' componentwise ⇒ L_x ≥ L_{x'}.
* In the real problem the monotonicity is even by numeric value of the p-free part.

**Generalization G\*** (tested, never failed):
* Setup: W is any divisor-closed set of integers > 1, with arbitrary positive
  multiplicity caps c_v.
* Take S = { ∏ v^{x_v} : 0 ≤ x_v ≤ c_v }.
* Claim: S is hole-free along any s whose proper divisors > 1 all lie in W, whether or
  not s ∈ W. That is, s·N and s^t·N in S, with N ∈ S, force s^j·N ∈ S for the j in
  between. (Note the base point N must be in S.)
* Special cases:
  * s = p, W = [2..n], caps 1: this is the conjecture itself.
  * s ∉ W: this is Lemma L (below).
* Scripts: `gprime.py`, `gcomp.py`.
* Holes DO appear along directions whose lower set is not contained in W, e.g. (1,−1,0)
  or (1,1,1) in 3-D (`dirs.py`). So the divisor-closed hypothesis is essential.
* 2-D is always hole-free (saturated), but that does not generalize.

---

## 4. Induction framework A (numeric order: add n = 2, 3, …)

Going from G = [n−1] to [n], write n = r·p^k with r p-free.

* **n = p^j:** only T0 grows. The reps are unchanged, so nothing to prove.
* **k ≥ 1:** chain r gets one more level (cap k → k+1). The new reps of class Y are
  Z = Q + r, where Q is a rep of Y/r with e_r(Q) = k.
* **k = 0** (p ∤ n): a new position n with cap 1. The new reps are Q + n.

**Lifting argument (PROVED).**
* M-connectivity of the old reps of each class carries over automatically, because
  M-adjacency does not depend on caps.
* The new reps are connected among themselves: lift a path between two Q's by adding r
  (or n) to every rep on it.
* So the only thing needed is **one M-edge between an old rep and a new rep** of the
  same class, whenever both kinds exist.

**When the bridge is automatic.** Suppose some rep Q of Y/r has e_r(Q) < k. Then Q + r is
itself an old rep (e_r ≤ k) and also lies on the new side. Equivalently, its interval
under the new cap contains placements that use level k and placements that avoid it.

**The "bad" case.** Every rep of Y/r has e_r = k.

**Empirical facts about bad cases** (`badrp.c`, exhaustive n ≤ 34; `bridge3.py`, n ≤ 22):

* **k ≥ 1:** a bad case occurs only with k = 1, r prime, r < p.
  * Examples: (n,p,r) = (6,3,2), (10,5,2), (14,7,2), (15,5,3), (21,7,3), (22,11,2),
    (26,13,2), (33,11,3), (34,17,2).
  * For n ≤ 22, every such case is bridged by merging the two copies of r into r²
    (M-move: −2 at r, +1 at r²). This works since r² < rp = n.
  * Rooms for r² in 23 ≤ n ≤ 34 were not checked.
  * **Unproved:** why k ≥ 2 or r ≥ p is never bad, and that r² always has room.
* **k = 0:** the minimal bridges (n ≤ 22), counting (Δ⁺, Δ⁻) relative to Q:

  | pattern | example | count |
  |---|---|---|
  | n → {a, b} with ab = n | 6 → {2,3} | 137,301 |
  | n → {a, a} | 9 → {3,3} | 260 |
  | Δ⁺ = {a, b}, Δ⁻ = {c} | 6·2 = 3·4 | 1,237 |
  | Δ⁺ = {a, b, c}, Δ⁻ = {d} | 9·4 = 2·3·6 | 8 |

  Never bigger than 4 elements for n ≤ 22.

**Equivalent inequality form (PROVED equivalences).**
* Let a(R) = min E_{n−1}(R) and b(R) = max E_{n−1}(R).
* The step n−1 → n is exactly:
  * (i) a(R/r) + k ≤ b(R) + 1
  * (ii) b(R/r) + k ≥ a(R) − 1

  whenever R and R/r both occur.
* **Complement symmetry:** x ↦ (n−1)!/x maps P_{n−1} to itself. Hence
  b(R) = v_p((n−1)!) − a(R*/R), where R* is the p-free part of (n−1)!.
* For k = 0, (ii) ⇔ (i) by complement, so only (i) is needed.
* Sufficient conditions via P1:
  * (i) holds if some rep e of R/r and some rep f of R have
    Σ_{e_s>f_s} C(e_s − f_s, 2) ≤ T0 − k + 1.
  * (ii) holds if some such pair has Σ_{f_s>e_s} C(f_s − e_s, 2) ≤ T0 + k + 1.
  * Here T0 ≥ C(k+1, 2), because p^k < n.
  * Checked exhaustively, n ≤ 22 (`realbad.py`).

---

## 5. Induction framework B (column order) — cleanest reduction found

Add whole columns (a p-free value x together with all its p-multiples x·p^i ≤ n) in
**increasing order of x**.

* This order is a linear extension of D, so every intermediate set is an order ideal.
* When column x is added, the ground set is W = {all p-free s < x}, with final caps
  L_s = ⌊log_p(n/s)⌋ + 1. So x is maximal: nothing in W is a multiple of x.
* Let L = L_x.
* Let [a_j, b_j] = E_W(R/x^j): the p-exponents achievable over W plus the pure chain,
  an interval by induction.
* Then
  E(R) = ⋃_{j=0}^{L} ( [a_j, b_j] + J_j ),  where J_j = [C(j,2), C(L,2) − C(L−j,2)].
* **Step 1 — the j's form an interval.** Lemma L below makes the set of j with R/x^j
  representable over W an interval.
* **Step 2 — consecutive pieces touch.** A short computation shows the pieces for j and
  j+1 overlap or touch iff
  * (α) a_{j+1} ≤ b_j + j(L − j − 1) + 1
  * (β) a_j ≤ b_{j+1} + j + (j+1)(L − j − 1) + 1
* **Step 3 — P1 plus slack give (α) and (β)** from the bridge lemma below. Take N = R/x^{j+1}.
  Given a rep f of N and a rep e of N·x (over W) such that f + [x] and e are M-adjacent,
  P1 with T0 ≥ C(L,2) yields both (α) and (β).

**So the whole conjecture reduces to two lemmas (§6), for W = p-free numbers < x with
monotone caps.**

---

## 6. THE TWO OPEN LEMMAS

Common setting:
* p prime, n ≥ x.
* W = { p-free s : 2 ≤ s < x }, with caps L_s = #{i ≥ 0 : s·p^i ≤ n}. The caps are
  ≥ 1 and non-increasing in s.
* x is p-free and composite (if x is prime both lemmas are vacuous: no element of W is
  divisible by x).
* "N representable" means N = ∏_{s∈W} s^{e_s} with 0 ≤ e_s ≤ L_s.

**Lemma L.** If N and N·x^t are representable (t ≥ 2), then N·x is representable.
(Iterating gives the full j-interval.)

**Bridge lemma.** If N and N·x are representable, then there are a rep f of N and a
rep e of N·x such that f + [x] and e are M-adjacent. Equivalently:
e = f + U⁺ − U⁻ with ∏U⁺ = x·∏U⁻, where U⁺ has at most one repeated element and U⁻ has
at most one.

**Evidence** (`colsetting.py`, every n ≤ 24, all p, all x):
* Lemma L: 0 failures.
* Bridge lemma: 0 failures in 1,156,064 cases.
  * 1,146,020 are "simple": f + {d, x/d} fits the caps for some f and some divisor d.
  * 10,044 need a genuine exchange.
* Abstract versions (arbitrary divisor-closed W, arbitrary caps, x maximal):
  * `maxs.py`: never "bad" in about 596k class checks.
  * `oimconn.py`: M-connectivity holds in 26,157 random classes.

---

## 7. Other PROVED facts worth reusing

* **Abstract capacity step.** Let c' = c + δ_s with c_s = k.
  * Then V_R(c') = V_R(c) ∪ (V_{R/s}(c) + k).
  * The union is fine unless every rep of R/s under c has e_s = k ("bad").
  * In the bad case all reps of R under c' have e_s ∈ {0, k+1}.
  * The decremented s may be chosen freely.
  * Raising the cap of an s that does not divide R changes nothing (e_s = 0, and
    lo/hi contributions are 0).
* **Duality.** hi(e) = T − lo(P/R complement rep), where T = Σ C(c,2). In the real
  problem this is the (n)!/x complement.
* **Lo-minimal reps.** In any lo-minimal rep, each chain is bottom-packed and contains no
  pure p-powers. With a Graver/conformal argument, lo-descent H1 is:
  * for each rep e with lo(e) > min, there is a rep f with lo(f) < lo(e) ≤ hi(f)+T0+1.

  H1 alone suffices for the conjecture (walk down from the max). H1 was verified for
  n ≤ 20 but is unproved; it is another possible route.
* **In the k ≥ 1 bad case of §4:**
  * every old rep X of Y has e_r(X) = 0;
  * any valid local move creating e_r ∈ [1, k] contradicts badness;
  * any split of r with room, or any merge r·y with room, contradicts badness.
  * These give strong structural constraints but no contradiction yet.

---

## 8. Dead ends (do NOT redo)

* **Pairwise overlap fails.** Two arbitrary reps' intervals can be far apart
  (e.g. n=20, p=3). Some kind of connectivity is needed. `pairwise.py`
* **Exchanges of 2 elements are not enough for lo-descent.** First failure: n=14, p=3,
  e={2,4,4,5,7,8}, which needs the 3-for-2 swap {4,5,7} → {10,14}. `h1small.py`
* **The "good s exists" test (`goods.py`, 318,451 classes, 0 failures) was misleading.**
  * It passed only because an s that does not divide R is trivially good.
  * For V = {3, 9} with caps (2, 1) and R = 9, no good s exists, yet the union is fine.
  * So the bad case must be handled directly.
* **Non-divisor-closed V fails.** Example: V = {2,3,10,18,27}, R = 27. (`gmodel.py`)
* **Arbitrary level offsets per chain fail**, so "virtual values" with shifted levels
  can't be used. (`gmodel.py`)
* **Saturation (S = lattice points of conv S) fails in 3-D** (`dirs.py`). So no
  polytope shortcut.
* **"Choose s maximal among values with cap ≥ 2" does not avoid bad cases.** Use s
  maximal in the whole of V (then it's Lemma L).
* **Minimal-distance-pair arguments.**
  * They give primitive relations (P, N) with no proper conformal sub-relation.
  * Local split/merge improvements are blocked only by capacity.
  * No argument yet bounds the blocked configurations. An earlier "minimal pair ⇒ no
    proper sub-exchange" proof had a flaw: sub-exchanges with δ < 0 or δ > d stay allowed.

---

## 9. Most promising lead (untried)

**For Lemma L: the t ≥ 2 valuation slack.**

Use this concrete plan (semiprime case first):
* Take x = a·b, a < b primes. Let Q be a rep of N and X a rep of N·x^t.
* Try inserting x's primes into Q in these ways:
  * add {a, b};
  * replace s by s·b and add a (for s < a);
  * replace s by s·a and add b;
  * replace s, s' by s·b, s'·a.
* If every option is blocked by caps, Q is *full* at b and at every b·w
  (w ∈ supp Q ∪ {1}, w < a), or full at a.
* Aim: show this forces v_b(∏Q) to equal the maximum b-valuation achievable over W, or
  to be within 1 of it. That contradicts v_b(∏X) = v_b(∏Q) + t ≥ v_b(∏Q) + 2.
* Two things help the counting: caps are monotone in value, and W contains *all*
  p-free numbers below x.
* **Gap in this plan:** fullness at the b·w with w ∉ supp Q isn't controlled yet. An
  augmenting-path / exchange argument (like matroid intersection) may be needed.

**Other ideas:**
* **Bridge lemma, k = 0.** Take a = the smallest prime factor of x and b = x/a. The
  simple bridge {a, b} fails only if every rep f of N is full at a or at b.
  * Then use a rep e of N·x: it has elements u = b·w (w < a) and u' = a·w'.
  * e − {u, u'} + {w, w'} is a rep of N and M-close to e.
  * Blocking again needs fullness at the small numbers w and w'. Try to turn that into a
    valuation contradiction as above.
* **Framework A (numeric order) alternative.** Prove "bad k ≥ 1 ⇒ k = 1, r prime,
  r < p" and "room at r²". Then the only bridge needed there is {r, r} → r².

---

## 10. Lean formalization plan (once a paper proof exists)

Suggested structure:

1. Reduce to p-free R and the set E_n(R). Use `Nat.factorization` or
   `ordProj`/`ordCompl` (`Nat.ordProj p x`, `Nat.ordCompl p x`).
2. Represent a subset by its count vector over p-free positions, plus the pure part.
3. Prove that a fixed rep gives an interval of exponents:
   * the sum of k distinct elements of {0..ℓ−1} ranges over [C(k,2), C(ℓ,2)−C(ℓ−k,2)];
   * induction on ℓ.
4. Prove P1.
5. Prove M-connectivity by induction on n (or by columns) using the two lemmas.
6. Discrete IVT: an M-connected family of intervals has an interval union.

Expect several thousand lines. Keep definitions `Finset`/`Multiset`-based, and avoid
`native_decide`. Check the final file with the validator pins of §2.

---

## 11. Repo layout

| path | contents |
|---|---|
| `lean/60957.lean` | upstream statement (read-only reference) |
| `c/sp.c` | bitmap verifier of the full conjecture (holds for n ≤ 46; `cc -O2 sp.c -o sp && ./sp 40`) |
| `c/badrp.c` | fast search for k ≥ 1 bad cases in framework A (n ≤ 34 done) |
| `scripts/exhaustive/` | real-setting checks: `mconn.py` (M-connectivity n ≤ 20), `realbad.py`, `bridge3.py`, `colsetting.py` (Lemma L + bridge, n ≤ 24), `k0.py`, `lodesc.py`/`h1small.py` (lo-descent), `wgap.py` (strong form without p-powers, n ≤ 34), `bigtest.py` (restricted prime sets up to n = 10^6) |
| `scripts/random-abstract/` | divisor-closed / order-ideal generalizations: `oimconn.py`, `oideal.py`, `gprime.py`, `gcomp.py`, `dirs.py`, `maxs.py`, `goods.py`, `badres.py`, `allbad*.py`, `chainbad.py`, `k2bad.py`, `gmodel.py`, `abstract*.py` |
| `scripts/lemma-probes/` | older lemma experiments (level order, transfers, bridges, minimal pairs) |
| `scripts/dead-ends/` | scripts behind §8 |

Most scripts take `N0 N` or `seed trials …` arguments. They need Python 3 and `sympy`.
`satur.py` needs `numpy`/`scipy` and was never run.

---

## 12. Context

* **Goal.** The target is a Lean proof of `OeisA60957.conjecture` in DeepMind `formal-conjectures`.
  Nothing counts until it compiles with no `sorry`.
* **Where things stand.** The paper proof is incomplete (see `PROOF.md`), and no Lean work exists.
