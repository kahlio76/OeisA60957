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
