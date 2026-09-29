import sys
from sympy import primerange
from math import comb
exec(open('lodesc.py').read().split('def adm')[0].split('N=int')[0])
N0=int(sys.argv[1]);N=int(sys.argv[2])
exec('def allreps'+open('lodesc.py').read().split('def allreps')[1].split('def adm')[0])
def small_moves(e,m,p,ell):
    d=dict(e); U=list(ell)
    def ok(x,delta): return 0<=d.get(x,0)+delta<=ell[x]
    res=[]
    # merge a,b -> ab ; split c->a,b ; swap ab=cd
    have=[x for x in U if d.get(x,0)>0]
    for i,a in enumerate(have):
        for b in have[i:]:
            if a==b and d[a]<2: continue
            ab=a*b
            # merge
            if ab in ell:
                dd=dict(d); dd[a]-=1; dd[b]-=1; dd[ab]=dd.get(ab,0)+1
                if dd[ab]<=ell[ab]: res.append(dd)
            # swap to c,d
            for c in U:
                if ab%c==0 and ab//c in ell:
                    dd2=ab//c
                    if c>dd2 or c in (a,b): continue
                    dd=dict(d); dd[a]-=1; dd[b]-=1; dd[c]=dd.get(c,0)+1; dd[dd2]=dd.get(dd2,0)+1
                    if dd[c]<=ell[c] and dd[dd2]<=ell[dd2]: res.append(dd)
    for c in have:
        for a in U:
            if c%a==0 and c//a in ell and a<=c//a:
                b=c//a; dd=dict(d); dd[c]-=1; dd[a]=dd.get(a,0)+1; dd[b]=dd.get(b,0)+1
                if dd[a]<=ell[a] and dd[b]<=ell[b]: res.append(dd)
    return res
for m in range(N0,N+1):
    for p in primerange(2,m+1):
        U=[r for r in range(2,m+1) if r%p]
        ell={}
        for r in U:
            k=0;x=r
            while x<=m:k+=1;x*=p
            ell[r]=k
        reps=allreps(m,p); fails=0
        for R,lst in reps.items():
            los=[sum(comb(c,2) for r,c in e) for e in lst]; lmin=min(los)
            for e,l in zip(lst,los):
                if l>lmin:
                    if not any(sum(comb(c,2) for c in f.values())<l for f in small_moves(e,m,p,ell)):
                        fails+=1
                        if fails<=3: print('FAIL m=%d p=%d R=%d e=%s lo=%d min=%d'%(m,p,R,e,l,lmin),flush=True)
        if fails: print('m',m,'p',p,'fails',fails,flush=True)
    print('done',m,flush=True)
