import numpy as np
from scipy.linalg import eigvals
import time

class SingularityEngine:
    def __init__(self, dim=16, epsilon=0.01, max_iterations=500, seed=None):
        self.dim=dim; self.epsilon=float(epsilon); self.max_iterations=int(max_iterations); self.iterations=0; self.history=[]
        if seed is not None: np.random.seed(seed)
        self.state=np.random.randn(self.dim)*0.1
    def metric(self):
        return np.eye(self.dim)+self.epsilon*np.outer(self.state,self.state)
    def metric_inverse_closed_form(self):
        s=self.state; coeff=self.epsilon/(1.0+self.epsilon*float(np.dot(s,s)))
        return np.eye(self.dim)-coeff*np.outer(s,s)
    def logdet_metric_closed_form(self):
        return np.log(1.0+self.epsilon*float(np.dot(self.state,self.state)))
    def spectral_radius(self,A): return float(np.max(np.abs(eigvals(A))))
    def max_real_part(self,A): return float(np.max(np.real(eigvals(A))))
    def evolve_state(self,dt=0.001): self.state=self.state-dt*self.state
    def execute_phase_transition(self):
        start_time=time.time()
        for _ in range(self.max_iterations):
            G_inv=self.metric_inverse_closed_form(); scale=1.0+0.001*self.iterations; A=-scale*G_inv
            lambda_max_real=self.max_real_part(A); rho=self.spectral_radius(A); self.evolve_state(); self.iterations+=1
            if self.iterations%100==0:
                self.history.append({'iter':self.iterations,'dim':self.dim,'lambda_max_real':lambda_max_real,'spectral_radius':rho,'entropy_proxy':0.5*self.logdet_metric_closed_form()})
        final_A=-(1.0+0.001*self.iterations)*self.metric_inverse_closed_form()
        return {'execution_time_sec':time.time()-start_time,'final_lambda_max_real':self.max_real_part(final_A),'final_spectral_radius':self.spectral_radius(final_A),'final_entropy_proxy':0.5*self.logdet_metric_closed_form(),'total_iterations':self.iterations,'milestones':self.history}
