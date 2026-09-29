import random, sys, itertools
from collections import defaultdict, Counter
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); d=int(sys.argv[3]); M=int(sys.argv[4]); MAXD=int(sys.argv[5])
def downclose(gens):
    D=set()
    for g in gens:
        for v in itertools.product(*[range(x+1) for x in g]):
            if any(v): D.add(v)
    return D
def reps(L):
    # L: position -> cap ; returns y -> list of dict e
    dp={tuple([0]*(d-1)):[{}]}
    for x,c in L.items():
        nd=defaultdict(list)
        for y,lst in dp.items():
            for j in range(c+1):
                y2=tuple(a+j*b for a,b in zip(y,x))
                for e in lst:
                    ee=dict(e)
                    if j: ee[x]=j
                    nd[y2].append(ee)
        dp=nd
    return dp
st=Counter()
for t in range(T):
    gens=[tuple(random.randint(0,M) for _ in range(d)) for _ in range(random.randint(1,4))]
    D=downclose(gens)
    if len(D)>MAXD: continue
    L=defaultdict(int)
    for v in D:
        x=v[1:]
        if any(x): L[x]=max(L[x],v[0]+1)
    maxw=[w for w in D if not any(u!=w and all(a<=b for a,b in zip(w,u)) for u in D)]
    for w in maxw:
        k=w[0]; x=w[1:]
        if not any(x) or k==0: continue
        Lp=dict(L); Lp[x]=k
        R=reps(Lp)
        for y,lst in R.items():
            y2=tuple(a+b for a,b in zip(y,x))
            if y2 not in R: continue
            # y2 reps with e_x=0 exist? (under Lp all reps of y2 are candidates)
            # bad: every rep of y has e_x==k
            if all(e.get(x,0)==k for e in lst):
                st['bad']+=1
                if st['bad']<=5: print('BAD D=%s w=%s y=%s'%(sorted(D),w,y),lst[:3],flush=True)
            else: st['good']+=1
print(st)
