import pytest
import math
from render import volumetric_cloud as mod

CASES = [
    ("steps", 'm.step_count(10, 2) == 20'),
    ("mip", 'm.mip_for_step(4) == 2'),
    ("phase", 'm.hg_phase(0, 0) == approx(0.079577, rel=1e-5)'),
    ("shadow", 'm.shadow_step(0.5, 4) == 2.0'),
    ("noise", 'm.noise_offset(2.5, 2) == approx(1.0)'),
    ("trans", 'm.blend_transmittance(0.5, 0.5) == approx(0.25)'),
    ("edge", 'm.upsample_edge(0.1, 0.2) is True'),
    ("reproj", 'm.reproject((0.5, 0.5), (0.1, 0.2)) == approx((0.4, 0.3))'),
    ("layers", 'm.separate_layers(1, 2) == (1, 2)'),
    ("jitter", 'm.jitter_count(64, 4) == 16'),
    ("far", 'm.far_density(0.2, 0.8, 0.5) == approx(0.5)'),
    ("od", 'm.optical_depth(2, 3) == approx(6.0)'),
    ("trans2", 'm.transmittance(1) == approx(0.367879, rel=1e-5)'),
    ("cov", 'm.coverage(0.5, 0.3) == 1.0'),
    ("id", 'm.cloud_id(3, 2) == "3:2"')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
