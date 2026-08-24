import numpy as np
from scipy.linalg import eigvals
import time

class RicciFlowWoodburyEngine:
    def __init__(self,n=64,k=4,eps0=0.01,gamma=0.1,max_it=500,dt=0.001,seed=42):
        self.n=n; self.k=k; self.eps=eps0; self.gamma=gamma; self.max_it=max_it; self.dt=dt; self.history=[]
        if seed is not None: np.random.seed(seed)
        self.S=np.random.randn(n,k)*0.5
    def compute_curvature_proxy(self): return 4.0*self.eps**2*np.linalg.norm(self.S)**4
    def ricci_adaptation_step(self): self.eps=max(self.eps-self.gamma*self.compute_curvature_proxy()*self.dt,1e-6)
    def woodbury_inverse(self):
        inner=np.eye(self.k)+self.eps*self.S.T@self.S; return np.eye(self.n)-self.eps*self.S@np.linalg.inv(inner)@self.S.T
    def spectral_radius(self,A): return float(np.max(np.abs(eigvals(A))))
    def max_real_part(self,A): return float(np.max(np.real(eigvals(A))))
    def run(self):
        start=time.time()
        for it in range(self.max_it):
            self.ricci_adaptation_step(); curvature=self.compute_curvature_proxy(); A=-(1.0+0.001*it)*self.woodbury_inverse(); rho=self.spectral_radius(A); lam=self.max_real_part(A); entropy=0.5*np.log(np.linalg.det(np.eye(self.k)+self.eps*self.S.T@self.S)+1e-30); self.S-=self.dt*self.S
            if (it+1)%100==0: self.history.append({'iter':it+1,'eps':self.eps,'curvature':curvature,'rho':rho,'lam_max':lam,'entropy':entropy})
        return {'exec_time':time.time()-start,'milestones':self.history}
