/* Claim* search: for each p-free r in [2,n] choose 0<=a_r<=b_r<=ell_r (D+ = levels [0,a), D- = [b,ell)).
   Local rules (Lemma 6.12/6.12') on every triple r*r2=s, balance of p-free parts, report
   excess E = sum C(a,2) - sum_{j=b}^{ell-1} j, its distribution, and extremal configs.  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 400
int n, p, K, cnt, ord[MAXN], pos[MAXN], ell[MAXN], a[MAXN], b[MAXN], asg[MAXN];
int nfac[MAXN], fq[MAXN][10], fe[MAXN][10], lp[MAXN];
int ntr[MAXN], tr[MAXN][200][3];          /* triples whose last-assigned member is r */
int gend[MAXN]; int endq[MAXN][10], nend[MAXN];
int bal[MAXN];                              /* prime exponent balance */
long long hist[4000]; int best = -100000; long long nodes = 0, LIMIT;
int SHOW, shown = 0; long long st_need[8], st_nodiv[8], st_stuck[8];
static int mm(int r){ return ell[r]-b[r]; }
static int check(int r, int r2, int s){
  int A=a[s], B=b[s];
  if (r!=r2){ if (a[r]>=1 && a[r2]>=1){ int lim = a[r]+a[r2]-1; if (lim>ell[s]) lim=ell[s]; if (A<lim) return 0; } }
  else { if (a[r]>=2){ int lim=2*a[r]-2; if (lim>ell[s]) lim=ell[s]; if (A<lim) return 0; } }
  int xs[2][2] = {{r,r2},{r2,r}}; int nx = (r==r2)?1:2;
  for (int t=0;t<nx;t++){ int x=xs[t][0], y=xs[t][1];
    if (a[x]>=1 && mm(s)>=1 && b[y]>=1){ int mx = (x!=y || b[y]>a[x]) ? (a[x]-1)+(b[y]-1) : 2*a[x]-3;
      if (mx>=0 && B<mx+1) return 0; }
    if (A>=1 && mm(x)>=1 && a[y]<ell[y]){ int mn;
      if (x!=y || a[y]<b[x]) mn=b[x]+a[y]; else mn = (mm(x)<2)? 1000 : 2*b[x]+1;
      if (A>mn) return 0; }
  }
  if (mm(r)>=1 && mm(r2)>=1 && B>=1){ int lim = (r!=r2)? b[r]+b[r2] : 2*b[r]+1; if (B>lim) return 0; }
  return 1;
}
static int excess(void){ int E=0; for (int i=0;i<cnt;i++){ int r=ord[i]; E += a[r]*(a[r]-1)/2; for (int j=b[r];j<ell[r];j++) E-=j; } return E; }
static void dfs(int i){
  if (++nodes > LIMIT) return;
  if (i==cnt){ int E=excess(); hist[E+2000]++; if (E>best) best=E;
    /* for each t>=1 and each chain r with a_r>t: is there a D- element at level >= t in a chain r' divisible by r (r'!=r)? */
    for (int t=1;t<8;t++){ int need=0, nodiv=0, stuck=0;
      for(int u=0;u<cnt;u++){ int r=ord[u]; if(a[r]<=t) continue; need++;
        int found=0, onlystuck=0;
        for(int w=0;w<cnt;w++){ int r2=ord[w]; if(r2==r || r2%r) continue; if (ell[r2]-1 < t) continue;
          int top=ell[r2]-1; if (b[r2]<=top && top>=t){ int uu=r2/r; if (b[uu]>=1) found=1; else onlystuck=1; } }
        if(!found){ if(onlystuck) stuck++; else nodiv++; } }
      if (need){ st_need[t]+=need; st_nodiv[t]+=nodiv; st_stuck[t]+=stuck; } }
    if (E>=1 && shown<SHOW){ shown++; printf("  E=%d:",E); for(int t=0;t<cnt;t++){int r=ord[t]; if(a[r]||b[r]<ell[r]) printf(" %d(a%d,b%d,l%d)",r,a[r],b[r],ell[r]);} printf("\n"); }
    return; }
  int s=ord[i];
  for (int A=0;A<=ell[s];A++) for (int B=A;B<=ell[s];B++){
    a[s]=A; b[s]=B; asg[s]=1; int ok=1;
    for (int t=0;t<ntr[s] && ok;t++) ok=check(tr[s][t][0],tr[s][t][1],tr[s][t][2]);
    if (ok){ int d=A-(ell[s]-B); for(int f=0;f<nfac[s];f++) bal[fq[s][f]]+=fe[s][f]*d;
      for (int e=0;e<nend[i] && ok;e++) if (bal[endq[i][e]]!=0) ok=0;
      if (ok) dfs(i+1);
      for(int f=0;f<nfac[s];f++) bal[fq[s][f]]-=fe[s][f]*d; }
    asg[s]=0;
  }
}
int main(int argc,char**argv){
  n=atoi(argv[1]); p=atoi(argv[2]); LIMIT=atoll(argv[3]); SHOW=argc>4?atoi(argv[4]):0;
  int L=0,v=p; while(v<=n){L++; v*=p;} 
  int R[MAXN], nr=0;
  for (int r=2;r<=n;r++) if (r%p){ R[nr++]=r; int k=0; long long w=r; while(w<=n){k++; w*=p;} ell[r]=k;
    int x=r; nfac[r]=0; for(int q=2;q<=x;q++) if(x%q==0){int e=0; while(x%q==0){x/=q;e++;} fq[r][nfac[r]]=q; fe[r][nfac[r]]=e; nfac[r]++; lp[r]=q;} }
  /* order by largest prime desc, then value asc */
  cnt=nr; for(int i=0;i<nr;i++) ord[i]=R[i];
  for(int i=0;i<nr;i++) for(int j=i+1;j<nr;j++){ int x=ord[i],y=ord[j];
    if (lp[y]>lp[x] || (lp[y]==lp[x] && y<x)){ ord[i]=y; ord[j]=x; } }
  for(int i=0;i<nr;i++) pos[ord[i]]=i;
  for(int i=0;i<nr;i++){ int q=lp[ord[i]]; gend[q]=i; }
  memset(nend,0,sizeof nend);
  for(int q=2;q<=n;q++) if (gend[q] || (q<=n && q%p && lp[q]==q)) ;
  for(int i=0;i<nr;i++){ int q=lp[ord[i]]; int last=1; for(int j=i+1;j<nr;j++) if(lp[ord[j]]==q) last=0; if(last){ endq[i][nend[i]++]=q; } }
  for(int si=0;si<nr;si++){ int s=R[si]; for(int ri=0;ri<nr;ri++){ int r=R[ri]; if(r*r>s) break; if(s%r==0 && (s/r)%p && s/r>=2){ int r2=s/r;
      int last=s; if(pos[r]>pos[last]) last=r; if(pos[r2]>pos[last]) last=r2;
      int t=ntr[last]++; tr[last][t][0]=r; tr[last][t][1]=r2; tr[last][t][2]=s; } } }
  dfs(0);
  printf("n %d p %d L %d T0 %d nodes %lld%s maxE %d  hist:", n,p,L,L*(L+1)/2,nodes,nodes>LIMIT?" (TRUNCATED)":"",best);
  printf("\n"); for(int t=1;t<4;t++) printf("  t%d: chains needing a partner %lld, no divisible D- partner at all %lld, only all-D- cofactor partners %lld\n",t,st_need[t],st_nodiv[t],st_stuck[t]);
}
