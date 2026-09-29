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
def madj(e,f):
    pos=[e.get(k,0)-f.get(k,0) for k in set(e)|set(f)]
    return sum(1 for x in pos if x>=2)<=1 and sum(1 for x in pos if x<=-2)<=1
st=Counter()
for t in range(T):
    gens=[tuple(random.randint(0,M) for _ in range(d)) for _ in range(random.randint(1,4))]
    D=downclose(gens)
    if len(D)>MAXD: continue
    L=defaultdict(int)
    for v in D:
        if any(v[1:]): L[v[1:]]=max(L[v[1:]],v[0]+1)
    R=reps(L)
    for y,lst in R.items():
        if len(lst)<2: continue
        seen={0}; stck=[0]
        while stck:
            i=stck.pop()
            for j in range(len(lst)):
                if j not in seen and madj(lst[i],lst[j]): seen.add(j); stck.append(j)
        if len(seen)<len(lst):
            st['DISC']+=1
            if st['DISC']<=3: print('DISC',sorted(D),y,lst[:4],flush=True)
        else: st['ok']+=1
print(st)
