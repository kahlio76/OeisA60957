# Session 2 scripts (2026-09-29)

All need Python 3 + sympy. Run from this directory (they import each other's `*_lib.py`).
"Framework B setting" = W = p-free numbers < x, caps ℓ_s = #{i ≥ 0 : s p^i ≤ n}.
"Profile scan" = small x, and n ranging over every threshold s·p^k where some cap changes (n up to NMAX).
This matters: several statements that hold for all n ≤ 24 fail only at n ≈ 40–250.

| script | what it tests | result so far |
|---|---|---|
| `common.py` | helpers: real caps, full rep enumeration | – |
| `locality.py N0 N1` | Lemma L: max over reps Q of min distance to a rep of Nx | ≤ 4 for n ≤ 23 |
| `simple_ins.py`, `canon.py`, `canon_fast.py` | Lemma L via "simple insertion" from a canonical rep | holds n ≤ 24; **fails** at larger n (see PROOF.md Part V.3) |
| `lexascent.py N0 N1 [small\|large]` | lex-ascent: every non-lex-max rep has an M-adjacent lex-greater rep | holds n ≤ 22 (small), n ≤ 16 (large) |
| `lamoves.py`, `upw.py` | size of the needed lex-ascent / UP_w moves | moves grow with n (unbounded) |
| `sigreedy.py`, `greedybridge.py`, `gg.py`, `gg_large.py`, `gg_random.py`, `gg_abstract2.py` | greedy-rep versions of Lemma L / bridge | all **fail** somewhere (PROOF.md Part V) |
| `profscan.py XMAX NMAX [PMAX] [SMAX]` | Lemma L + bridge themselves over all cap profiles | 0 failures, x ≤ 15, n ≤ 400 |
| `minpair.py XMAX NMAX` | min-distance bridge pairs are M-adjacent | 1,026,838 instances (x ≤ 16, n ≤ 150), all M-adjacent; shapes (0,2),(1,2),(1,3) only |
| `shorten.py` | how big a ratio-1 move is needed to shorten a non-M-adjacent bridge pair | (running) |
| `geodesic.py N0 N1 CAP` | geodesic property for MC in the core world | holds n ≤ 22 |
| `geoprof.py` | geodesic property on sub-worlds with large-n caps | (to rerun) |
| `verify_partV.py` | independent check of the PROOF.md Part V counterexamples | all confirmed |
| `samecore.py XMAX NMAX` | bridge pairs sharing the same x-free core multiset | exist and can be M-adjacent in all tested non-prime-power cases; 216 exceptions, all x = 9 |
| `twostep.py XMAX NMAX` | two-step single-move route Q → Y → X for x with ≥ 2 primes | 525,172 instances, 0 failures |
| `locmin.py XMAX NMAX K PAIRMAX [semi]` | pairs not shortenable by ratio-1 moves of ≤ K blocks | semiprimes: K=3 ⇒ M-adjacent (≈3.3M), K=4 ⇒ also \|D⁻\| ≤ 1 |
| `nonmadj_moves.py`, `nonmadj_moves2.py` | which merge/split moves shorten non-M-adjacent semiprime pairs | every one has a shortening merge/split (≈3.5M) |
| `lip.py`, `lip2.py`, `lipgen.py`, `lipv.py`, `lipmoves.py` | Lipschitz row/column boundaries of 2-prime slices (PROOF Part IV route (Lip)) | slope-1 version fails in general worlds; direction-aware version: some orientation always holds so far |
| `convF.py` | is the 2-prime slice lattice-convex? | yes for semiprimes x ≤ 15, **no** from x = 21 |
| `gpsize.py` | size of shortening M-moves in the geodesic property | (timed out) |
| `mccat.py X PMAX Pi mode` | cap-free (MC-cat)/(B-cat): non-M-adjacent relations with no ratio-1 / single-catalyst part | none found (PROOF Part VI.4) |
| `catshape.py X PMAX` | smallest certificate shape for (MC-cat) | size ≤ 3 except 16 cases (size 4–5), X = 17 |
| `pcat.py N0 N1` | (p-cat): certificates for all disjoint D⁺, D⁻ ⊆ [2,n], ratio p^t, t ≥ 2 | all have certificates, n ≤ 12 |
| `mcrand.py XMAX TRIALS CMAX` | MC and (L\*) with random non-monotone caps | 0 failures, X ≤ 14 |
| `pn_ally.py`, `pn_mixed.py` | fibers of P_n along every integer / rational ratio | intervals, n ≤ 26 / n ≤ 22 |
| `ylstar.py XMAX NMAX` | y-fibers of S(V) for all composite y, not just the next element | intervals, X ≤ 16 |
| `structcfg.py n p LIMIT` | Lemma-6.6 configurations with t ≥ 2: does a (p-cat) certificate exist? | always (n ≤ 50, p ∈ {3,5,7}, capped enumeration) |
| `primcat.py`, `randcat.py` | primitive non-M-adjacent relations: smallest single-catalyst part | always size ≤ 3 (X ≤ 17); none missing (random, X = 30, 40) |
| `bshape.py`, `bcat2.py` | ratio-x relations with \|D⁻\| ≥ 2: certificate shapes | always a certificate of size ≤ 4 (x ≤ 15) |
| `rulecfg2.py`, `rulecfg3.py n p` | exhaustive search of Setting-M colourings obeying the local rules (Lemmas 6.12, 6.12') + balance | max t = 1 − T0 (never ≥ 2); profit − cost ≤ 1 |
| `energy.py N0 N1` | energy gaps Σ C(g_r,2) among reps of each R | ≤ T0 + 1 for n ≤ 18 |
| `heavycat.py` | random heavy relations (Cor. 6.14) | (too slow as written) |
