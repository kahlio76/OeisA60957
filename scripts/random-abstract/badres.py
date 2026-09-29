import random, sys
from sympy import divisors
from collections import defaultdict, Counter
exec(open('goods.py').read().split('nobad=0')[0].split('random.seed')[0])
def reps(V,cap):
    dp=defaultdict(list); dp[1].append({})
    for v in sorted(V):
        c=cap[v]; nd=defaultdict(list)
        for R,lst in dp.items():
            for k in range(0,c+1):
                for d in lst:
                    dd=dict(d)
                    if k: dd[v]=k
                    nd[R*v**k].append(dd)
        dp=nd
    return dp
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); mode=sys.argv[3]
st=Counter()
def key(e): return tuple(sorted(e.items()))
for trial in range(T):
    gens=random.sample(range(2,36),random.randint(2,4))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    if mode=='mono':
        N=max(V); cap={v: max(1,min(3, 1+int((N/v)**0.5)-1)) for v in V}
    else:
        cap={v:(random.choice([2,3]) if random.random()<0.35 else 1) for v in V}
    full=reps(V,cap)
    for R,lst in full.items():
        for s in V:
            if cap[s]<2 or R%s: continue
            k=cap[s]-1
            Rs=[e for e in full.get(R//s,[]) if e.get(s,0)<=k]
            if not Rs or all(e.get(s,0)>=1 for e in lst) : continue
            if any(g.get(s,0)<k for g in Rs): continue
            # bad
            Xs=set(key(e) for e in lst if e.get(s,0)==0)
            Zs=[e for e in lst if e.get(s,0)>0]
            found=None
            for Z in Zs:
                ws=[[s*s]]+[[a,s*s//a] for a in divisors(s) if 1<a<s]
                for W in ws:
                    if any(w not in V for w in W): continue
                    X=dict(Z); X[s]-=2
                    if X[s]<0: continue
                    if X[s]==0: del X[s]
                    for w in W: X[w]=X.get(w,0)+1
                    if key(X) in Xs: found=len(W);break
                if found: break
            maxl = all(not(cap.get(m,0)>=2 and m!=s and m%s==0) for m in V)
            st[(k, found, 'max' if maxl else 'notmax')]+=1
            if not found and st[(k,found,'max' if maxl else 'notmax')]<=2:
                print(flush=True);print('UNRES s=%d k=%d R=%d V=%s cap=%s'%(s,k,R,sorted(V),{v:cap[v] for v in sorted(V) if cap[v]>1}))
                for e in lst[:8]: print('   ',e)
print(st)
