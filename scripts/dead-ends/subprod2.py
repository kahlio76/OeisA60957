import sys
from sympy import primerange
S={1}
for n in range(2,int(sys.argv[1])+1):
    S|={s*n for s in S}
    if n<17: continue
    bad=0; mx=max(S)
    for p in primerange(2,n+1):
        for m in S:
            if m*p in S: continue
            # m*p not in S: check whether any higher power times m is in S
            q=m*p*p
            while q<=mx:
                if q in S:
                    bad+=1
                    if bad<=3: print('COUNTEREX n=%d p=%d m=%d'%(n,p,m),flush=True)
                    break
                q*=p
    # note: only checks k=1 gap relative to each m; gaps at higher k are covered by taking m'=p^j m in S
    print(n,len(S),'bad',bad,flush=True)
