import math

def step_count(depth, density):
    """自适应步数。"""
    raise NotImplementedError("TODO: step_count")

def mip_for_step(step):
    """按步长选 mip。"""
    raise NotImplementedError("TODO: mip_for_step")

def hg_phase(cos_theta, g):
    """多次散射相函数。"""
    raise NotImplementedError("TODO: hg_phase")

def shadow_step(main_step, ratio):
    """阴影步进。"""
    raise NotImplementedError("TODO: shadow_step")

def noise_offset(time, speed):
    """噪声偏移。"""
    raise NotImplementedError("TODO: noise_offset")

def blend_transmittance(front, back):
    """透射率混合。"""
    raise NotImplementedError("TODO: blend_transmittance")

def upsample_edge(depth_delta, threshold):
    """上采样保边。"""
    raise NotImplementedError("TODO: upsample_edge")

def reproject(uv, motion):
    """时域重投影。"""
    raise NotImplementedError("TODO: reproject")

def separate_layers(cloud, fog):
    """雾云分层。"""
    raise NotImplementedError("TODO: separate_layers")

def jitter_count(steps, samples):
    """抖动采样数。"""
    raise NotImplementedError("TODO: jitter_count")

def far_density(near, far, t):
    """远近密度过渡。"""
    raise NotImplementedError("TODO: far_density")

def optical_depth(density, distance):
    """光学深度。"""
    raise NotImplementedError("TODO: optical_depth")

def transmittance(od):
    """透射率。"""
    raise NotImplementedError("TODO: transmittance")

def coverage(density, threshold):
    """覆盖率。"""
    raise NotImplementedError("TODO: coverage")

def cloud_id(seed, index):
    """云 id。"""
    raise NotImplementedError("TODO: cloud_id")
