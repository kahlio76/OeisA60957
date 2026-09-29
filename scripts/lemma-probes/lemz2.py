import sys
from sympy import primerange, divisors
from collections import defaultdict, Counter
N=int(sys.argv[1])
def reps_over(caps):
    reps=defaultdict(list); reps[1].append({})
    for r,c in caps.items():
        if c==0: continue
        nr=defaultdict(list)
        for R,lst in reps.items():
            for e in range(0,c+1):
                for d in lst:
                    dd=dict(d)
                    if e: dd[r]=e
                    nr[R*r**e].append(dd)
        reps=nr
    return reps
stats=Counter()
for n in range(4,N+1):
    for p in primerange(2,n+1):
        vals=[r for r in range(2,n+1) if r%p]
        full={}
        for r in vals:
            k=0;x=r
            while x<=n:k+=1;x*=p
            full[r]=k
        for s in vals:
            caps={r:full[r] for r in vals if r<s}
            reps=reps_over(caps)
            for Rs,glist in reps.items():
                R=Rs*s
                if R not in reps: continue
                O=reps[R]
                A=False
                for g in glist:
                    for a in divisors(s):
                        b=s//a
                        if a<2 or a>b: continue
                        if a==b and g.get(a,0)+2<=caps.get(a,0): A=True
                        if a!=b and g.get(a,0)+1<=caps.get(a,0) and g.get(b,0)+1<=caps.get(b,0): A=True
                        if A: break
                    if A: break
                B=False
                import itertools
                for e in O:
                    parts=[r for r,c in e.items() for _ in range(c)]
                    for k in range(2,6):
                        for idx in itertools.combinations(range(len(parts)),k):
                            X=[parts[i] for i in idx]; pr=1
                            for x in X: pr*=x
                            if pr%s: continue
                            y=pr//s
                            if y==1 or (y<s and y in caps and e.get(y,0)+1<=caps.get(y,0)): B=k;break
                        if B:break
                    if B:break
                stats[(A,B if not A else True)]+=1
                if not A and not B and stats[(A,B)]<=5: print('NEITHER n=%d p=%d s=%d R=%d g=%s O=%s'%(n,p,s,R,glist[:2],O[:2]))
    if n%4==0: print('n',n,dict(stats),flush=True)
print(dict(stats))
