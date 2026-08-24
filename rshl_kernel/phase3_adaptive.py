import numpy as np
from scipy.linalg import eigvals
import time

class AdaptiveWoodburyEngine:
    def __init__(self,n=64,k=4,eps0=0.01,alpha=10.0,max_it=500,dt=0.001,seed=42):
        self.n=n; self.k=k; self.eps0=eps0; self.alpha=alpha; self.max_it=max_it; self.dt=dt; self.history=[]
        if seed is not None: np.random.seed(seed)
        self.S=np.random.randn(n,k)*0.5
    def get_adaptive_eps(self): return self.eps0/(1.0+self.alpha*np.linalg.norm(self.S)**2)
    def get_eps_gradient(self,current_eps):
        coeff=-(2.0*self.alpha*current_eps)/(1.0+self.alpha*np.linalg.norm(self.S)**2); return coeff*self.S
    def woodbury_inverse(self,current_eps):
        inner=np.eye(self.k)+current_eps*self.S.T@self.S; return np.eye(self.n)-current_eps*self.S@np.linalg.inv(inner)@self.S.T
    def calculate_entropy_and_gradient(self,current_eps):
        inner=np.eye(self.k)+current_eps*self.S.T@self.S; inv=np.linalg.inv(inner); entropy=0.5*np.log(np.linalg.det(inner)+1e-30); geom=current_eps*self.S@inv; eps_grad=self.get_eps_gradient(current_eps); overlap=np.trace(inv@(self.S.T@self.S)); return entropy,geom+0.5*eps_grad*overlap
    def spectral_radius(self,A): return float(np.max(np.abs(eigvals(A))))
    def max_real_part(self,A): return float(np.max(np.real(eigvals(A))))
    def run(self):
        start=time.time()
        for it in range(self.max_it):
            eps=self.get_adaptive_eps(); A=-(1.0+0.001*it)*self.woodbury_inverse(eps); rho=self.spectral_radius(A); lam=self.max_real_part(A); entropy,grad=self.calculate_entropy_and_gradient(eps); self.S-=self.dt*self.S
            if (it+1)%100==0: self.history.append({'iter':it+1,'eps':eps,'rho':rho,'lam_max':lam,'entropy':entropy,'grad_norm':np.linalg.norm(grad)})
        return {'exec_time':time.time()-start,'milestones':self.history}
