import random, sys, itertools
from collections import defaultdict
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); d=int(sys.argv[3]); M=int(sys.argv[4])
def downclose(gens):
    D=set()
    for g in gens:
        for v in itertools.product(*[range(x+1) for x in g]):
            if any(v): D.add(v)
    return D
def sums(D):
    S={tuple([0]*d)}
    for w in D:
        S|={tuple(a+b for a,b in zip(s,w)) for s in S}
    return S
def fibers(S):
    F=defaultdict(list)
    for s in S: F[s[1:]].append(s[0])
    return {k:(min(v),max(v),len(v)) for k,v in F.items()}
def maximal(D): return [w for w in D if not any(u!=w and all(a<=b for a,b in zip(w,u)) for u in D)]
badH=badK=cross=0; tests=0
for t in range(T):
    gens=[tuple(random.randint(0,M) for _ in range(d)) for _ in range(random.randint(1,4))]
    D=downclose(gens)
    if len(D)>16: continue
    S=sums(D); F=fibers(S)
    for k,(a,b,l) in F.items():
        if b-a+1!=l: badH+=1; print('HOLE',sorted(D),k,flush=True)
    for w in maximal(D):
        Dp=D-{w}; Fp=fibers(sums(Dp)); w1=w[0]; wp=w[1:]
        for y,(a,b,l) in Fp.items():
            y2=tuple(p+q for p,q in zip(y,wp))
            if y2 in Fp:
                a2,b2,_=Fp[y2]; tests+=1
                if not (a2<=b+w1+1 and a+w1<=b2+1):
                    badK+=1; print('KFAIL',sorted(D),w,y,flush=True)
print('tests',tests,'badH',badH,'badK',badK)
