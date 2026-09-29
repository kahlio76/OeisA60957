import sys
from sympy import primerange, divisors
from collections import defaultdict, Counter
exec(open('realbad.py').read().split('st=Counter()')[0].split('N0=int')[0])
exec('def allreps'+open('realbad.py').read().split('def allreps')[1].split('st=Counter()')[0])
N0=int(sys.argv[1]); N=int(sys.argv[2])
st=Counter()
for n in range(N0,N+1):
    for p in primerange(2,n):
        if n%p==0: continue
        facs=[(a,n//a) for a in divisors(n) if 1<a<=n//a]
        if not facs: continue
        reps,ell=allreps(n-1,p)
        for R,lst in reps.items():
            if R*n not in reps: continue
            ok=False
            for e in lst:
                for a,b in facs:
                    if a%p==0 or b%p==0: continue
                    if a==b:
                        if e.get(a,0)+2<=ell[a]: ok=True;break
                    elif e.get(a,0)<ell[a] and e.get(b,0)<ell[b]: ok=True;break
                if ok: break
            st[ok]+=1
            if not ok and st[False]<=5:
                print('NOSPLIT n=%d p=%d R=%d reps=%s'%(n,p,R,lst[:3]),flush=True)
    print('done',n,dict(st),flush=True)
