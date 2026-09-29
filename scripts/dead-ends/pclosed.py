import random, sys
from collections import defaultdict
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
def check(D,p):
    V=defaultdict(set); V[1].add(0)
    for x in D:
        v=vp(x,p); u=x//p**v
        new=defaultdict(set)
        for R,s in V.items(): new[R]|=s; new[R*u]|={a+v for a in s}
        V=new
    for R,s in V.items():
        if max(s)-min(s)+1!=len(s): return R,sorted(s)
random.seed(1); p=2; found=0
for trial in range(20000):
    base=random.sample([x for x in range(3,40,2)],random.randint(2,5))
    D=set()
    for b in base:
        k=random.randint(0,3)
        for j in range(k+1): D.add(b*2**j)
    r=check(sorted(D),p)
    if r:
        found+=1
        if found<=3: print('p-closed counterexample D=%s R=%d V=%s'%(sorted(D),r[0],r[1]))
print('found',found)
