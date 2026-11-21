"""Core helpers for volumetric cloud raymarching.

Each helper maps to one of the artefacts seen in the rendered frames:

* ``step_count``       -- sample count adapts to view depth instead of using a
                          fixed world-space step (no more hard stair steps).
* ``mip_for_step``     -- pick the density-texture mip from the step length so
                          low-frequency noise is not buried under detail.
* ``hg_phase``         -- Henyey-Greenstein phase used for the multiple
                          scattering approximation (warm cloud bases).
* ``shadow_step``      -- shadow ray steps follow the main step length, so the
                          cloud cannot shadow itself into stripes.
* ``noise_offset``     -- deterministic, time-continuous noise offset instead
                          of a per-frame random reset (no boiling).
* ``blend_transmittance`` -- compose two transmittance segments.
* ``upsample_edge``    -- depth-aware half-resolution upsample test.
* ``reproject``        -- history lookup using motion vectors.
* ``separate_layers``  -- keep clouds and translucent particles in separate
                          depth-sorted layers.
* ``jitter_count``     -- number of ray-march steps per blue-noise sample.
* ``far_density``      -- blend near/far cloud representations by density.
* ``optical_depth``    -- density integrated along the view ray.
* ``transmittance``    -- Beer-Lambert transmittance.
* ``coverage``         -- binary coverage against a density threshold.
* ``cloud_id``         -- stable identifier for a cloud instance.
"""

import math

# The noise field repeats every two world units; offsets wrap on that period so
# the value stays bounded while remaining a pure function of time.
NOISE_PERIOD = 2.0


def step_count(depth, density):
    """Return the number of raymarch samples needed to cover ``depth``.

    ``density`` is the sampling rate in samples per unit of view depth, so the
    budget is ``depth * density``.  Deriving the budget from each ray's own
    depth span means a ray that covers more world space is given more samples
    instead of marching a fixed world-space step until it happens to stop.
    """
    depth = max(0.0, float(depth))
    density = max(0.0, float(density))
    if depth == 0.0 or density == 0.0:
        return 0
    return max(1, int(round(depth * density)))


def mip_for_step(step):
    """Return the density-texture mip level for a world-space sample step.

    A step twice as long can be filtered with one extra mip level, so the mip
    is ``floor(log2(step))``.  Steps shorter than one world unit use mip 0.
    """
    step = float(step)
    if step <= 1.0:
        return 0
    return int(math.floor(math.log2(step)))


def hg_phase(cos_theta, g):
    """Henyey-Greenstein phase function.

    ``g`` is the scattering anisotropy in ``(-1, 1)``; ``g == 0`` gives the
    isotropic value ``1 / (4 * pi)``.  Used per scattering lobe to build the
    multiple-scattering approximation.
    """
    # Keep the denominator away from zero at the extreme anisotropies.
    g = max(-0.999, min(0.999, float(g)))
    cos_theta = max(-1.0, min(1.0, float(cos_theta)))
    denom = 1.0 + g * g - 2.0 * g * cos_theta
    return (1.0 - g * g) / (4.0 * math.pi * denom ** 1.5)


def shadow_step(main_step, ratio):
    """Return the shadow-ray step derived from the main ray step.

    Keeping the two in lockstep (within ``ratio``) prevents the alternating
    self-shadow bands produced by mismatched sampling.
    """
    return float(main_step) * float(ratio)


def noise_offset(time, speed):
    """Return the noise-field offset for ``time`` at the given speed.

    Deterministic and continuous in time; wrapping on ``NOISE_PERIOD`` keeps
    the offset bounded instead of letting the UV drift without limit.
    """
    return (float(time) * float(speed)) % NOISE_PERIOD


def blend_transmittance(front, back):
    """Compose the transmittance of two consecutive segments."""
    return max(0.0, min(1.0, float(front) * float(back)))


def upsample_edge(depth_delta, threshold):
    """Return ``True`` when a half-resolution sample may be bilinearly blended.

    Large depth deltas mark a silhouette, where naive upsampling would smear
    the cloud edge, so only samples within ``threshold`` are considered.
    """
    return abs(float(depth_delta)) <= float(threshold)


def reproject(uv, motion):
    """Reproject a UV through a motion vector (in UV space)."""
    return (float(uv[0]) - float(motion[0]), float(uv[1]) - float(motion[1]))


def separate_layers(cloud, fog):
    """Keep the cloud and translucent-particle layers separate for sorting."""
    return (cloud, fog)


def jitter_count(steps, samples):
    """Return how many raymarch steps share one blue-noise jitter sample."""
    steps = int(steps)
    samples = int(samples)
    if samples <= 0:
        return max(1, steps)
    return max(1, steps // samples)


def far_density(near, far, t):
    """Blend near and far cloud representations by density."""
    t = max(0.0, min(1.0, float(t)))
    near = float(near)
    far = float(far)
    return near + (far - near) * t


def optical_depth(density, distance):
    """Optical depth of a homogeneous medium: density times distance."""
    return max(0.0, float(density)) * max(0.0, float(distance))


def transmittance(od):
    """Beer-Lambert transmittance for an optical depth ``od``."""
    return math.exp(-max(0.0, float(od)))


def coverage(density, threshold):
    """Binary coverage of a sample given a density threshold."""
    return 1.0 if float(density) >= float(threshold) else 0.0


def cloud_id(seed, index):
    """Stable identifier for the ``index``-th cloud of a generation seed."""
    return "{}:{}".format(seed, index)
