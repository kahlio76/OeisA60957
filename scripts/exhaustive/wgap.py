import sys
from sympy import primerange
from collections import defaultdict
N=int(sys.argv[1])
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
for n in range(4,N+1):
    row=[]
    for p in primerange(2,n+1):
        L=0
        while p**(L+1)<=n: L+=1
        T1=L*(L+1)//2
        W=defaultdict(set); W[1].add(0)
        for x in range(2,n+1):
            v=vp(x,p); u=x//p**v
            if u==1: continue
            new=defaultdict(set)
            for R,s in W.items():
                new[R]|=s; new[R*u]|={a+v for a in s}
            W=new
        mg=0
        for R,s in W.items():
            s=sorted(s)
            for a,b in zip(s,s[1:]): mg=max(mg,b-a)
        row.append('p%d:gap%d/T1+1=%d'%(p,mg,T1+1))
    print(n,' '.join(row),flush=True)
