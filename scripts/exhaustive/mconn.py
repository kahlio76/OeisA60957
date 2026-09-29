import sys
from sympy import primerange
from math import comb
from collections import defaultdict, Counter
exec('def allreps'+open('realbad.py').read().split('def allreps')[1].split('st=Counter()')[0])
N0=int(sys.argv[1]); N=int(sys.argv[2]); mode=sys.argv[3]
def madj(e,f,T0,ell):
    keys=set(e)|set(f)
    pos=[e.get(k,0)-f.get(k,0) for k in keys]
    if mode=='P1':
        a=sum(comb(x,2) for x in pos if x>1); b=sum(comb(-x,2) for x in pos if x<-1)
        return a<=T0+1 and b<=T0+1
    big1=sum(1 for x in pos if x>=2); big2=sum(1 for x in pos if x<=-2)
    return big1<=1 and big2<=1
for n in range(N0,N+1):
    for p in primerange(2,n+1):
        reps,ell=allreps(n,p)
        L0=0;x=1
        while x*p<=n: x*=p;L0+=1
        T0=L0*(L0+1)//2
        bad=0
        for R,lst in reps.items():
            if len(lst)<2: continue
            seen={0}; stck=[0]
            while stck:
                i=stck.pop()
                for j in range(len(lst)):
                    if j not in seen and madj(lst[i],lst[j],T0,ell): seen.add(j); stck.append(j)
            if len(seen)<len(lst):
                bad+=1
                if bad<=2: print('DISCONN n=%d p=%d R=%d'%(n,p,R),[lst[i] for i in range(len(lst)) if i not in seen][:2],'vs',lst[0],flush=True)
        if bad: print('n',n,'p',p,'disconnected classes',bad,flush=True)
    print('done',n,flush=True)
