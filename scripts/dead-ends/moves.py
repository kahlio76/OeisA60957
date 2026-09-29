import sys, itertools
from collections import defaultdict, Counter
from sympy import primerange
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
n=int(sys.argv[1])
els=list(range(2,n+1))  # ignore 1 (irrelevant to products)
prod={}
for p in primerange(2,n+1):
    # enumerate all subsets as bitmasks
    m=len(els); best=defaultdict(int)
    info=[]
    P=[1]*(1<<m)
    for mask in range(1,1<<m):
        low=(mask&-mask).bit_length()-1; P[mask]=P[mask&(mask-1)]*els[low]
    for mask in range(1<<m):
        x=P[mask]; v=vp(x,p); R=x//p**v
        if v>best[R]: best[R]=v
    stats=Counter(); worst=None
    for mask in range(1<<m):
        x=P[mask]; v=vp(x,p); R=x//p**v
        if v==best[R]: continue
        # find minimal move: remove X subset of S, add Y subset of complement, prod Y = p*prod X, minimize |X|+|Y|
        S=[els[i] for i in range(m) if mask>>i&1]; C=[els[i] for i in range(m) if not mask>>i&1]
        found=None
        for size in range(1,7):
            for kx in range(0,size+1):
                ky=size-kx
                if ky==0: continue
                for X in itertools.combinations(S,kx):
                    px=1
                    for t in X: px*=t
                    target=px*p
                    for Y in itertools.combinations(C,ky):
                        py=1
                        for t in Y: py*=t
                        if py==target: found=(X,Y); break
                    if found: break
                if found: break
            if found: break
        key=(len(found[0]),len(found[1])) if found else None
        stats[key]+=1
        if key and (worst is None or sum(key)>sum(worst[0])): worst=(key,S,found)
    print('p=%d'%p, dict(stats), 'worst', worst, flush=True)
