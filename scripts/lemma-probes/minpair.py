import sys, itertools
from sympy import primerange
from collections import defaultdict
m=int(sys.argv[1])
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
for p in [int(a) for a in sys.argv[2].split(',')]:
    els=list(range(1,m+1))
    info={x:(vp(x,p), x//p**vp(x,p)) for x in els}
    # enumerate all subsets (m<=16)
    byR=defaultdict(list)
    for mask in range(1<<m):
        S=[els[i] for i in range(m) if mask>>i&1]
        v=sum(info[x][0] for x in S); R=1
        for x in S: R*=info[x][1]
        byR[R].append((v,frozenset(S)))
    shown=0
    for R,lst in byR.items():
        vals=set(v for v,S in lst)
        for v1,S in lst:
            # S up-saturated: no x in S with x*p<=m, x*p not in S ; and p in S
            if any(x*p<=m and x*p not in S for x in S) or (p not in S): continue
            for v2,T in lst:
                if v2<v1+2: continue
                if any(x%p==0 and x//p not in T for x in T) or p in T: continue
                X=S-T; Y=T-S
                # between set
                betw=[(len(U^S)+len(U^T),U,v) for v,U in lst if v1<v<v2]
                b=min(betw,key=lambda t:t[0])
                if shown<12:
                    shown+=1
                    print('p=%d R=%d S=%s(v%d) T=%s(v%d) X=%s Y=%s  U=%s(v%d)'%(p,R,sorted(S),v1,sorted(T),v2,sorted(X),sorted(Y),sorted(b[1]),b[2]))
