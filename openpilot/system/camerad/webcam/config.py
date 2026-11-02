"""Explicit, board-scoped settings for the Q8B road-camera experiment."""
import os

from openpilot.common.platform import RADXA_Q8B

ROAD_WIDTH, ROAD_HEIGHT = 1280, 720
CAPTURE_FPS, PUBLISH_FPS = 60, 20
AK_CAMERA = '/dev/v4l/by-id/usb-SunplusIT_Inc_AK-Camera_JV-video-index0'


def road_only_enabled() -> bool:
  value = os.getenv('Q8B_ROAD_ONLY', '0')
  if value not in ('0', '1'):
    raise ValueError('Q8B_ROAD_ONLY must be 0 or 1')
  if value == '1' and (not RADXA_Q8B or 'USE_WEBCAM' not in os.environ):
    raise ValueError('Q8B_ROAD_ONLY=1 requires Radxa Q8B and USE_WEBCAM')
  return value == '1'


def road_camera_device() -> str:
  if os.getenv('DRIVER_CAM') or os.getenv('WIDE_CAM'):
    raise ValueError('Remove DRIVER_CAM/WIDE_CAM for Q8B road-only mode')
  value = os.getenv('NARROW_ROAD_CAM', os.getenv('ROAD_CAM', AK_CAMERA))
  return f'/dev/video{value}' if value.isdecimal() else value


def rotate_180() -> bool:
  value = os.getenv('ROAD_CAM_ROTATE_180', '0')
  if value not in ('0', '1'):
    raise ValueError('ROAD_CAM_ROTATE_180 must be 0 or 1')
  return value == '1'


def stats_enabled() -> bool:
  value = os.getenv('Q8B_SHOW_STATS', '1')
  if value not in ('0', '1'):
    raise ValueError('Q8B_SHOW_STATS must be 0 or 1')
  return road_only_enabled() and value == '1'
