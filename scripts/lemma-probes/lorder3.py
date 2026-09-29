import sys
from sympy import primerange
from collections import defaultdict
exec(open('lorder.py').read().split('stats=Counter()')[0].split('N=int(sys.argv[1])')[1])
n=int(sys.argv[1]); p=int(sys.argv[2]); shown=0
vals=[r for r in range(2,n+1) if r%p]
full={}
for r in vals:
    k=0;x=r
    while x<=n:k+=1;x*=p
    full[r]=k
for s in vals:
    j=1
    if full[s]<=j: continue
    caps={r:min(full[r], j+1 if r<s else j) for r in vals}; caps[s]=j
    reps=reps_over(caps)
    for Rs,glist in reps.items():
        R=Rs*s
        if R not in reps: continue
        O=reps[R]
        if any(e.get(s,0)>=1 for e in O) or any(g.get(s,0)<j for g in glist): continue
        if shown<6:
            shown+=1
            print('s=%d R=%d  caps(<s)=%s'%(s,R,{r:caps[r] for r in vals if caps[r]}))
            print('   N (reps of R/s):',glist[:4],'... total',len(glist))
            print('   O (reps of R):',O[:4],'... total',len(O))
