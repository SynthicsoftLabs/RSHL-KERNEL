import numpy as np
from scipy.linalg import eigvals
import time

class WoodburyEngine:
    def __init__(self,n=64,k=4,eps=0.01,max_it=500,dt=0.001,seed=None):
        self.n=n; self.k=k; self.eps=float(eps); self.max_it=int(max_it); self.dt=float(dt); self.history=[]
        if seed is not None: np.random.seed(seed)
        self.S=np.random.randn(n,k)*0.1
    def woodbury_inverse(self):
        inner=np.eye(self.k)+self.eps*self.S.T@self.S
        return np.eye(self.n)-self.eps*self.S@np.linalg.inv(inner)@self.S.T
    def logdet(self):
        inner=np.eye(self.k)+self.eps*self.S.T@self.S
        return np.log(np.linalg.det(inner)+1e-30)
    def entropy_gradient(self):
        inner=np.eye(self.k)+self.eps*self.S.T@self.S
        return self.eps*self.S@np.linalg.inv(inner)
    def spectral_radius(self,A): return float(np.max(np.abs(eigvals(A))))
    def max_real_part(self,A): return float(np.max(np.real(eigvals(A))))
    def evolve_state(self): self.S=self.S-self.dt*self.S
    def run(self):
        start=time.time()
        for it in range(self.max_it):
            G_inv=self.woodbury_inverse(); A=-(1.0+0.001*it)*G_inv
            rho=self.spectral_radius(A); lam=self.max_real_part(A); entropy=0.5*self.logdet(); self.evolve_state(); grad_norm=np.linalg.norm(self.entropy_gradient())
            if (it+1)%100==0: self.history.append({'iter':it+1,'lambda_max_real':lam,'rho':rho,'entropy_proxy':entropy,'grad_norm':grad_norm})
        return {'exec_time':time.time()-start,'milestones':self.history}
