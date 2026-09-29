import sys
from sympy import primerange
from math import comb
from collections import defaultdict
M=int(sys.argv[1])
worst=None
for m in range(3,M+1):
    for p in primerange(2,m+1):
        U=[r for r in range(2,m+1) if r%p]
        ell={}
        for r in U:
            k=0; x=r
            while x<=m: k+=1; x*=p
            ell[r]=k
        k=0; x=1
        while x<=m: k+=1; x*=p
        T1=comb(k,2)
        # per R track max lo and min hi over reps
        st={1:(0,0)}
        for r in U:
            nr={}
            for R,(ml,mh) in st.items():
                for e in range(0,ell[r]+1):
                    la=comb(e,2); ha=comb(ell[r],2)-comb(ell[r]-e,2)
                    RR=R*r**e; val=(ml+la,mh+ha)
                    if RR in nr: nr[RR]=(max(nr[RR][0],val[0]),min(nr[RR][1],val[1]))
                    else: nr[RR]=val
            st=nr
        fails=[(R,ml,mh) for R,(ml,mh) in st.items() if ml>mh+T1+1]
        slack=min(mh+T1+1-ml for R,(ml,mh) in st.items())
        if fails: print('m=%d p=%d T1=%d FAIL count=%d example=%s'%(m,p,T1,len(fails),fails[:3]),flush=True)
        if worst is None or slack<worst[0]: worst=(slack,m,p)
    if m%10==0: print('checked',m,'worst slack',worst,flush=True)
