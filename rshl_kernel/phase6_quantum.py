import numpy as np
from scipy.linalg import expm
from scipy.spatial.distance import pdist,squareform
import time

class QuantumTopologicalEngine:
    def __init__(self,n=64,k=4,eps0=0.01,gamma=0.1,max_it=500,dt=0.001,dt_quantum=0.05,seed=42):
        self.n=n; self.k=k; self.eps=eps0; self.gamma=gamma; self.max_it=max_it; self.dt=dt; self.dt_quantum=dt_quantum; self.history=[]; self.transitions=[]
        if seed is not None: np.random.seed(seed)
        self.S=np.random.randn(n,k)*.5; psi=np.random.randn(n)+1j*np.random.randn(n); self.psi=psi/np.linalg.norm(psi)
    def compute_curvature_proxy(self): return 4*self.eps**2*np.linalg.norm(self.S)**4
    def ricci_adaptation_step(self): self.eps=max(self.eps-self.gamma*self.compute_curvature_proxy()*self.dt,1e-6)
    def get_graph_properties(self):
        d=squareform(pdist(self.S)); t=np.percentile(d[d>0],50)*(1+2*self.compute_curvature_proxy()); a=(d<=t).astype(float); return a,np.sum(a,axis=1)
    def build_hamiltonian(self,a,degrees,curvature):
        J=2*(1+5*curvature); V=-10*(degrees/np.max(degrees+1e-6)); return -J*a+np.diag(V)
    def evolve_quantum_state(self,H): self.psi=expm(-1j*H*self.dt_quantum)@self.psi; self.psi/=np.linalg.norm(self.psi)
    def compute_quantum_metrics(self):
        p=np.abs(self.psi)**2; ipr=np.sum(p**2); ph=np.angle(self.psi); return ipr,float(np.sqrt(np.mean(np.cos(ph))**2+np.mean(np.sin(ph))**2))
    def run(self):
        start=time.time(); prev=None
        for it in range(self.max_it):
            self.ricci_adaptation_step(); c=self.compute_curvature_proxy(); a,d=self.get_graph_properties(); self.evolve_quantum_state(self.build_hamiltonian(a,d,c)); ipr,coh=self.compute_quantum_metrics(); self.S-=self.dt*self.S
            if prev is not None and abs(ipr-prev)>.002: self.transitions.append({'iter':it+1,'curvature':c,'ipr':ipr,'phase_coherence':coh,'delta_ipr':abs(ipr-prev)})
            prev=ipr
            if (it+1)%100==0: self.history.append({'iter':it+1,'eps':self.eps,'curvature':c,'ipr':ipr,'phase_coherence':coh})
        return {'exec_time':time.time()-start,'milestones':self.history,'quantum_transitions':self.transitions}
