// For n up to N: for each prime p<n, n=r p^k (k>=1, r>1): compute reachable p-free products over positions != r (caps),
// then find A with: A/r^k reachable (so A has rep with e_r=k), A/r^j unreachable for j<k, A*r reachable w/o r.
// report r vs p and whether r^{k+1}<=n-1.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
// represent products by exponent vectors over primes < n (excluding p) packed... simpler: use hash set of u128? products can be huge.
// Use exponent vectors: primes up to 40 -> 11 primes; exponents bounded; pack into u64 with 6 bits each (max exponent 63).
int primes[20],np;
int N;
#define HS (1<<24)
u64 *tab; char *used;
static u64 hsh(u64 x){x^=x>>33;x*=0xff51afd7ed558ccdULL;x^=x>>33;return x;}
int ins(u64 *t,char *u,u64 x){u64 h=hsh(x)&(HS-1);while(u[h]){if(t[h]==x)return 0;h=(h+1)&(HS-1);}u[h]=1;t[h]=x;return 1;}
int has(u64 *t,char *u,u64 x){u64 h=hsh(x)&(HS-1);while(u[h]){if(t[h]==x)return 1;h=(h+1)&(HS-1);}return 0;}
u64 vec(int x,int p){u64 v=0;for(int i=0;i<np;i++){int q=primes[i];if(q==p)continue;int e=0;while(x%q==0){x/=q;e++;}v+=(u64)e<<(6*i);}return v;}
int main(int argc,char**argv){
  N=atoi(argv[1]);
  for(int q=2;q<=N;q++){int ok=1;for(int d=2;d*d<=q;d++)if(q%d==0)ok=0;if(ok)primes[np++]=q;}
  u64 *A=malloc(HS*8),*B=malloc(HS*8); char *ua=malloc(HS),*ub=malloc(HS);
  u64 *list=malloc(sizeof(u64)*HS), *nl=malloc(sizeof(u64)*HS);
  for(int n=4;n<=N;n++){
   for(int pi=0;pi<np;pi++){int p=primes[pi]; if(p>=n)break;
    int r=n,k=0; while(r%p==0){r/=p;k++;} if(k==0||r==1)continue;
    // positions: p-free s in [2,n-1], s!=r, caps L_s
    memset(ua,0,HS); int cnt=1; list[0]=0; ins(A,ua,0);
    for(int s=2;s<n;s++){ if(s%p==0||s==r)continue; int L=0; long x=s; while(x<n){L++;x*=p;}
      u64 v=vec(s,p); int c0=cnt;
      for(int i=0;i<c0;i++){u64 b=list[i]; for(int j=1;j<=L;j++){u64 y=b+v*j; if(ins(A,ua,y)){ if(cnt>=HS/2){fprintf(stderr,"overflow\n");return 1;} list[cnt++]=y;}}}
    }
    u64 vr=vec(r,p); int bad=0,badrp=0;
    // A (target) = b + k*vr for b in list (reachable w/o r). need: b + (k-j)*vr unreachable w/o r for j... 
    // A/r^j reachable-without-r means A - j*vr in set. A = b + k vr (so A/r^k = b reachable).
    for(int i=0;i<cnt;i++){u64 b=list[i]; u64 Av=b+vr*k; int ok=1;
      for(int j=0;j<k;j++){ // A/r^j = b + (k-j) vr
        if(has(A,ua,b+vr*(k-j))){ok=0;break;} }
      if(!ok)continue;
      if(!has(A,ua,Av+vr))continue; // A*r reachable without r
      bad++; long rk=1; for(int j=0;j<=k;j++) rk*=r;
      if(rk>n-1) badrp++;
    }
    if(bad) printf("n=%d p=%d r=%d k=%d bad=%d bad_with_r^(k+1)>n-1: %d\n",n,p,r,k,bad,badrp);
   }
   fprintf(stderr,"done %d\n",n);
  }
}
