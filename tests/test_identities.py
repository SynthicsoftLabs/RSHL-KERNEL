import numpy as np
from rshl_kernel import WoodburyEngine

def test_woodbury_inverse_identity():
    n,k,eps=64,4,.01; S=np.random.randn(n,k)*.1; G=np.eye(n)+eps*S@S.T; truth=np.linalg.inv(G); inner=np.eye(k)+eps*S.T@S; wb=np.eye(n)-eps*S@np.linalg.inv(inner)@S.T; assert np.allclose(truth,wb,atol=1e-8)

def test_sylvester_determinant_identity():
    n,k,eps=64,4,.01; S=np.random.randn(n,k)*.1; dn=np.linalg.det(np.eye(n)+eps*S@S.T); dk=np.linalg.det(np.eye(k)+eps*S.T@S); assert np.isclose(dn,dk,atol=1e-8)

def test_engine_execution():
    engine=WoodburyEngine(n=32,k=2,eps=.01,max_it=50,dt=.001,seed=42); result=engine.run(); assert result['exec_time']>0; assert len(result['milestones'])>0
