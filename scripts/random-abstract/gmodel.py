import random, sys, itertools
from collections import defaultdict
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); closed=int(sys.argv[3]); gapfree=int(sys.argv[4])
from sympy import divisors
def sums(M,e):
    return set(sum(c) for c in itertools.combinations(M,e))
def check(V,Ms):
    # dp over values: R -> set of sums (as union), but need union over reps of sum sets: dp R-> set of achievable totals (all combos) - that's exactly union
    dp={1:{0}}
    for v in V:
        M=Ms[v]; nd=defaultdict(set)
        for R,S in dp.items():
            for e in range(len(M)+1):
                ss=sums(M,e)
                nd[R*v**e]|={a+b for a in S for b in ss}
        dp=nd
    for R,S in dp.items():
        if max(S)-min(S)+1!=len(S): return R,sorted(S)
    return None
bad=0
for t in range(T):
    if closed:
        gens=random.sample(range(2,40),random.randint(2,3)); V=set()
        for g in gens: V|=set(d for d in divisors(g) if d>1)
    else:
        V=set(random.sample(range(2,30),random.randint(2,5)))
    V=sorted(V)
    Ms={}
    for v in V:
        c=random.choice([1,1,1,2,2,3])
        if gapfree:
            a=random.randint(0,2); M=[a+i for i in range(c)]
            M+= [random.randint(a,a+c-1) for _ in range(random.choice([0,0,1]))]
        else:
            M=list(range(c))
        Ms[v]=M
    r=check(V,Ms)
    if r:
        bad+=1
        if bad<=5: print('FAIL',V,Ms,r)
print('bad',bad)
