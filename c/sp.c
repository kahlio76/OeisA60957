#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
int n; int np; int pr[20]; int bits[20]; int off[20]; u64 mask;
u64 vec(int x){ u64 v=0; for(int i=0;i<np;i++){int e=0; while(x%pr[i]==0){x/=pr[i];e++;} v|=(u64)e<<off[i];} return v; }
int main(int c,char**argv){ n=atoi(argv[1]);
  // primes <= n excluding those > n/2 (free singletons)
  np=0; int tot=0;
  for(int p=2;p<=n;p++){int ip=1; for(int d=2;d*d<=p;d++) if(p%d==0) ip=0; if(!ip) continue; if(2*p>n) continue;
     int e=0; for(int q=p;q<=n;q*=p) e+=n/q; // v_p(n!)
     int b=0; while((1<<b)<=e) b++; pr[np]=p; bits[np]=b; off[np]=tot; tot+=b; np++; }
  fprintf(stderr,"n=%d primes(<=n/2)=%d bits=%d\n",n,np,tot);
  u64 size=1ULL<<tot; unsigned char *R=calloc(size/8+1,1);
  #define GET(v) ((R[(v)>>3]>>((v)&7))&1)
  #define SET(v) (R[(v)>>3]|=1<<((v)&7))
  SET(0);
  for(int x=2;x<=n;x++){ u64 vx=vec(x); if(!vx) continue; // x with only large primes: free
    // iterate downward over v to avoid reuse: process in decreasing order
    for(u64 v=size-1;;v--){ if(GET(v)){ u64 w=v+vx; // check no field overflow: fields sized to max so sum stays in field
        SET(w);} if(v==0) break; } }
  long bad=0;
  for(int i=0;i<np;i++){ u64 ep=1ULL<<off[i];
    for(u64 v=0;v<size;v++) if(GET(v)){ u64 fv=(v>>off[i])&((1ULL<<bits[i])-1); u64 maxf=(1ULL<<bits[i])-1;
       if(fv+1<=maxf && !GET(v+ep)){ for(u64 k=2;fv+k<=maxf;k++) if(GET(v+k*ep)){bad++; if(bad<5) printf("COUNTEREX n=%d p=%d vec=%llx gap\n",n,pr[i],v); break;} } } }
  long cnt=0; for(u64 v=0;v<size;v++) cnt+=GET(v);
  printf("n=%d reachable(p<=n/2 part)=%ld bad=%ld\n",n,cnt,bad); }
