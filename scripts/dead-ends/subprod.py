import sys
from sympy import primerange
def products(n):
    S={1}
    for k in range(2,n+1):
        S|={s*k for s in S}
    return S
for n in range(2,int(sys.argv[1])+1):
    S=products(n); bad=0
    for p in primerange(2,n+1):
        for m in S:
            # find max a with p^a*m in S; check all intermediate
            q=m*p; k=1; seen=[]
            while q<= max(S):
                if q in S: seen.append(k)
                q*=p; k+=1
            if seen:
                top=max(seen)
                missing=[j for j in range(1,top) if j not in seen]
                if missing:
                    bad+=1
                    if bad<=3: print('COUNTEREX n=%d p=%d m=%d have exps %s missing %s'%(n,p,m,seen,missing))
    print(n,len(S),'bad',bad,flush=True)
