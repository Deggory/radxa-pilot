"""Finite tensor diagnostics shared by host conversion and the lightweight Q8B replay."""
import numpy as np


def errors(reference, actual):
  if reference.shape != actual.shape or not np.isfinite(reference).all() or not np.isfinite(actual).all():
    raise ValueError('nonfinite or mismatched output')
  difference = actual.astype(np.float64) - reference.astype(np.float64)
  scale = float(np.sqrt(np.mean(reference.astype(np.float64) ** 2)))
  return {'bitwise_equal': reference.dtype == actual.dtype and reference.tobytes() == actual.tobytes(),
          'mae': float(np.mean(np.abs(difference))), 'max_abs': float(np.max(np.abs(difference))),
          'relative_rms': float(np.sqrt(np.mean(difference ** 2)) / scale) if scale > 1e-12 else None,
          'outside_atol_0p01_rtol_0p01': int(np.sum(np.abs(difference) > .01 + .01 * np.abs(reference)))}

