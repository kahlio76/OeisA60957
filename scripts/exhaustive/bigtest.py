import sys, itertools
from math import comb
def test(n,p,primes):
    # values: products of given primes (<=n), p-free
    vals=[1]
    for q in primes:
        new=[]
        for v in vals:
            x=v
            while x<=n: new.append(x); x*=q
        vals=sorted(set(new))
    vals=[v for v in vals if v>1]
    def exps(v):
        e=[]
        for q in primes:
            k=0
            while v%q==0: v//=q;k+=1
            e.append(k)
        return tuple(e)
    maxe=[0]*len(primes)
    for v in vals:
        for i,k in enumerate(exps(v)): maxe[i]=max(maxe[i],k)
    # bound exponents of R to keep state small: allow up to sum over chains... cap total exponent per prime to limit
    LIM=[min(3*m+6,40) for m in maxe]
    dp={tuple([0]*len(primes)):1}   # state -> bitmask of valuations
    for v in vals:
        c=0;x=v
        while x<=n: c+=1;x*=p
        ev=exps(v)
        ndp=dict(dp)
        for st,mask in dp.items():
            for k in range(1,c+1):
                ns=tuple(st[i]+k*ev[i] for i in range(len(primes)))
                if any(ns[i]>LIM[i] for i in range(len(primes))): break
                lo=comb(k,2); hi=lo+k*(c-k)
                sh=0
                for t in range(lo,hi+1): sh|=mask<<t
                ndp[ns]=ndp.get(ns,0)|sh
        dp=ndp
    bad=0
    for st,mask in dp.items():
        b=bin(mask)[2:][::-1]
        s=b.index('1'); e=len(b)-1-b[::-1].index('1')
        if '0' in b[s:e+1]:
            bad+=1
            if bad<=3: print('  GAP n=%d p=%d R-exps=%s valuations=%s'%(n,p,st,[i for i,ch in enumerate(b) if ch=='1']))
    return bad,len(dp)
for n in [100,1000,10**4,10**5,10**6]:
    for p,pr in [(5,(2,3)),(7,(2,3)),(3,(2,5)),(11,(2,3)),(7,(2,3,5)),(13,(2,3,5))]:
        if len(pr)==3 and n>10**5: continue
        b,ns=test(n,p,pr)
        print('n=%d p=%d primes=%s states=%d gaps=%d'%(n,p,pr,ns,b),flush=True)
