"""
RSHL-KERNEL: Rivers State-Hamiltonian Learning Framework
"""
__version__ = "1.0.0"

from .phase1_rank1 import SingularityEngine
from .phase2_rankk import WoodburyEngine
from .phase3_adaptive import AdaptiveWoodburyEngine
from .phase4_ricci_flow import RicciFlowWoodburyEngine
from .phase5_topology import TopologicalRicciFlowEngine
from .phase6_quantum import QuantumTopologicalEngine
from .phase7_holographic import HolographicProjectionEngine
from .phase8_retrocausal import RetrocausalHolographicEngine
from .phase9_convergence import IdentityConvergenceEngine

__all__ = [
    "SingularityEngine", "WoodburyEngine", "AdaptiveWoodburyEngine",
    "RicciFlowWoodburyEngine", "TopologicalRicciFlowEngine",
    "QuantumTopologicalEngine", "HolographicProjectionEngine",
    "RetrocausalHolographicEngine", "IdentityConvergenceEngine",
]
