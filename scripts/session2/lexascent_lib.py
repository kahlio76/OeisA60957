# Test "lex-ascent": in the core world of the real problem (p-free s in [2,n], caps = chain lengths),
# every rep e of N that is not lex-max has an M-adjacent rep f of N with f >_lex e.
# Lex order: count vector indexed by increasing s (so lex-max prefers small elements).
# Usage: lexascent.py N0 N1 [order]  order in {small, large}
import sys
from collections import Counter
from sympy import primerange
from common import all_reps

def madj(e, f):
    up = dn = 0
    for a, b in zip(e, f):
        d = b - a
        if d >= 2:
            up += 1
            if up > 1: return False
        elif d <= -2:
            dn += 1
            if dn > 1: return False
    return True

