import numpy as np
from scipy.linalg import eigvals
from scipy.spatial.distance import pdist,squareform
import time

class TopologicalRicciFlowEngine:
    def __init__(self,n=64,k=4,eps0=0.01,gamma=0.1,max_it=500,dt=0.001,seed=42):
        self.n=n; self.k=k; self.eps=eps0; self.gamma=gamma; self.max_it=max_it; self.dt=dt; self.history=[]; self.topological_transitions=[]
        if seed is not None: np.random.seed(seed)
        self.S=np.random.randn(n,k)*0.5
    def compute_curvature_proxy(self): return 4*self.eps**2*np.linalg.norm(self.S)**4
    def ricci_adaptation_step(self): self.eps=max(self.eps-self.gamma*self.compute_curvature_proxy()*self.dt,1e-6)
    def woodbury_inverse(self):
        inner=np.eye(self.k)+self.eps*self.S.T@self.S; return np.eye(self.n)-self.eps*self.S@np.linalg.inv(inner)@self.S.T
    def _count_connected_components(self,a):
        n=a.shape[0]; seen=np.zeros(n,bool); c=0
        for i in range(n):
            if not seen[i]:
                c+=1; q=[i]; seen[i]=1
                while q:
                    for j in np.where(a[q.pop()]==1)[0]:
                        if not seen[j]: seen[j]=1; q.append(j)
        return c
    def _estimate_loops(self,a): return max(0,int(np.sum(a)//2)-a.shape[0]+self._count_connected_components(a))
    def _estimate_voids(self,a,points,threshold): return 0
    def compute_persistent_homology_approx(self):
        d=squareform(pdist(self.S)); vals=d[d>0]; out=[]
        for t in np.percentile(vals,[10,25,50,75,90]):
            a=(d<=t).astype(int); out.append((self._count_connected_components(a),self._estimate_loops(a),self._estimate_voids(a,self.S,t)))
        return out
    def detect_topological_transition(self,c,p): return p is not None and c!=p
    def spectral_radius(self,A): return float(np.max(np.abs(eigvals(A))))
    def max_real_part(self,A): return float(np.max(np.real(eigvals(A))))
    def run(self):
        start=time.time(); prev=None; current=None
        for it in range(self.max_it):
            self.ricci_adaptation_step(); curvature=self.compute_curvature_proxy(); A=-(1+.001*it)*self.woodbury_inverse(); rho=self.spectral_radius(A); lam=self.max_real_part(A); entropy=.5*np.log(np.linalg.det(np.eye(self.k)+self.eps*self.S.T@self.S)+1e-30)
            if (it+1)%10==0:
                current=self.compute_persistent_homology_approx()
                if self.detect_topological_transition(current,prev): self.topological_transitions.append({'iter':it+1,'curvature':curvature,'betti_change':current,'prev_betti':prev})
                prev=current
            self.S-=self.dt*self.S
            if (it+1)%100==0: self.history.append({'iter':it+1,'eps':self.eps,'curvature':curvature,'rho':rho,'lam_max':lam,'entropy':entropy,'betti':current})
        return {'exec_time':time.time()-start,'milestones':self.history,'topological_transitions':self.topological_transitions}
