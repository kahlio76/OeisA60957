import random, sys
from math import comb
from sympy import divisors
random.seed(int(sys.argv[1])); T=int(sys.argv[2])
def run(V,cap):
    dp={1:1}
    for v in sorted(V):
        c=cap[v]
        if c==0: continue
        nd=dict(dp)
        for R,mask in dp.items():
            for k in range(1,c+1):
                lo=comb(k,2); hi=lo+k*(c-k); sh=0
                for t in range(lo,hi+1): sh|=mask<<t
                RR=R*v**k
                nd[RR]=nd.get(RR,0)|sh
        dp=nd
    for R,mask in dp.items():
        b=bin(mask)[2:][::-1]; s=b.index('1'); e=len(b)-1-b[::-1].index('1')
        if '0' in b[s:e+1]: return R,[i for i,ch in enumerate(b) if ch=='1']
bad=0
for trial in range(T):
    gens=random.sample(range(2,60),random.randint(2,5))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    # monotone caps: assign random caps then enforce c(v)>=c(w) if v|w
    cap={v:random.randint(1,4) for v in V}
    changed=True
    while changed:
        changed=False
        for v in V:
            for w in V:
                if w%v==0 and cap[v]<cap[w]: cap[v]=cap[w]; changed=True
    r=run(V,cap)
    if r:
        bad+=1
        if bad<=3: print('COUNTEREX V=%s cap=%s R=%d vals=%s'%(sorted(V),cap,r[0],r[1]))
print('bad',bad,'of',T)
