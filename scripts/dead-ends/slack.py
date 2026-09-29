import sys
from sympy import primerange
from collections import defaultdict
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
N=int(sys.argv[1])
for p in primerange(2,N//2+1):
    # maintain dict R -> (min,max) over subsets of [k]
    mm={1:(0,0)}
    tight1=[];tight2=[]; minslack1=99; minslack2=99
    for k in range(2,N+1):
        t=vp(k,p); s=k//p**t
        new=dict(mm)
        for R,(a,b) in mm.items():
            R2=R*s; a2,b2=a+t,b+t
            if R2 in mm and s>1:
                A,B=mm[R2]
                # L1: min_{R2/s}+t <= max_{R2}+1 ; L2: min_{R2} <= max_{R2/s}+t+1
                s1=B+1-a2; s2=b2+1-A
                if s1<minslack1: minslack1=s1
                if s2<minslack2: minslack2=s2
                if s1==0: tight1.append((k,R2))
                if s2==0: tight2.append((k,R2))
                new[R2]=(min(A,a2),max(B,b2))
            else:
                new[R2]=(a2,b2) if R2 not in new else (min(new[R2][0],a2),max(new[R2][1],b2))
        mm=new
    print('p=%d N=%d minslack L1=%d L2=%d tight1=%d tight2=%d ex1=%s ex2=%s'%(p,N,minslack1,minslack2,len(tight1),len(tight2),tight1[:3],tight2[:3]),flush=True)
