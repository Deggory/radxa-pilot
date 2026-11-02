"""Extract paired road tensors with the project's pinned CPU warp; no model inference."""
import argparse
from bisect import bisect_right
from collections import Counter
import hashlib
import json
import os
from pathlib import Path

import numpy as np


def digest(path):
  h = hashlib.sha256()
  with Path(path).open('rb') as f:
    for chunk in iter(lambda: f.read(8 << 20), b''):
      h.update(chunk)
  return h.hexdigest()


def desire_pulse(state, direction, previous):
  # Recorded starting-state metadata reconstructs conditioning; it is not an
  # observation of the original model input. Keep this limit in the manifest.
  index = {'left': 3, 'right': 4}.get(direction, 0) if state == 'laneChangeStarting' else 0
  current = np.zeros(8, dtype=np.float32)
  current[index] = 1
  pulse = np.where(current - previous > .99, current, 0)
  pulse[0] = 0
  return pulse, current


def presentation_indices(entries, segment):
  selected = [entry for entry in entries if entry.segmentNum == segment and str(entry.type) == 'fullHEVC']
  mapping = {entry.frameId: entry.segmentId for entry in selected}
  if len(mapping) != len(selected) or len(set(mapping.values())) != len(mapping):
    raise ValueError('duplicate frame/presentation index in selected video segment')
  return mapping


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--source', required=True, type=Path)
  parser.add_argument('--output', required=True, type=Path)
  parser.add_argument('--frames', type=int, default=700)
  args = parser.parse_args()
  if not 1 <= args.frames <= 1200:
    parser.error('frames must be between 1 and 1200')
  if args.output.exists():
    parser.error('output already exists; choose a new directory')
  # Late imports keep pure conditioning helpers testable without a media stack.
  import zstandard as zstd
  os.environ['DEV'] = 'CPU:LLVM'
  from tinygrad import Tensor, Device
  if Device.DEFAULT != 'CPU' or Device.default.renderer.target.renderer != 'LLVM':
    raise ValueError('run extraction in a fresh CPU:LLVM process')
  from examples.openpilot.compile_warp import NV12Frame, make_frame_prepare
  from openpilot.cereal import log
  from openpilot.common.transformations.camera import DEVICE_CAMERAS
  from openpilot.common.transformations.model import get_warp_matrix
  from openpilot.tools.lib.framereader import FrameReader

  with (args.source / 'rlog.zst').open('rb') as f, zstd.ZstdDecompressor().stream_reader(f) as stream:
    events = list(log.Event.read_multiple_bytes(stream.read()))
  groups = {}
  for event in events:
    groups.setdefault(event.which(), []).append(event)
  timestamps = {name: [e.logMonoTime for e in values] for name, values in groups.items()}

  def latest(name, timestamp):
    index = bisect_right(timestamps[name], timestamp) - 1
    if index < 0:
      raise ValueError(f'no prior {name} at timestamp {timestamp}')
    return groups[name][index]

  first_valid_time = max(groups[name][0].logMonoTime for name in ['extrinsicsCalibration', 'drivingModelData'])
  narrow = [(i, event) for i, event in enumerate(groups['narrowRoadCameraState'])
            if event.logMonoTime >= first_valid_time][:args.frames]
  wide_by_id = {e.wideRoadCameraState.frameId: e for e in groups['wideRoadCameraState']}
  encode_positions = {name: presentation_indices([getattr(event, name) for event in groups[name]], 4)
                      for name in ['narrowRoadEncodeIdx', 'wideRoadEncodeIdx']}
  if len(narrow) != args.frames:
    raise ValueError('insufficient route frames')
  device = groups['deviceState'][0].deviceState
  camera_key = (str(device.deviceType), str(narrow[0][1].narrowRoadCameraState.sensor))
  camera = DEVICE_CAMERAS[camera_key]
  cp = groups['carParams'][0].carParams
  dm_name = 'driverMonitoringState' if 'driverMonitoringState' in groups else 'driverMonitoringStateDEPRECATED'
  dm = getattr(groups[dm_name][0], dm_name)
  traffic = np.array([[0., 1.] if dm.isRHD else [1., 0.]], dtype=np.float32)
  readers = [FrameReader(str(args.source / filename), pix_fmt='nv12', cache_size=2, hwaccel='none')
             for filename in ['fcamera.hevc', 'ecamera.hevc']]
  configs = [camera.narrow_road, camera.wide_road]
  prepares = []
  for reader, config in zip(readers, configs, strict=True):
    if (reader.w, reader.h) != config.size:
      raise ValueError('logged camera/video dimensions differ')
    prepares.append(make_frame_prepare(NV12Frame(reader.w, reader.h, reader.w, reader.h, reader.h // 2,
                                               reader.w * reader.h * 3 // 2), 512, 256))
  args.output.mkdir(parents=True)
  previous = np.zeros(8, dtype=np.float32)
  records, counts = [], Counter()
  for index, (source_index, event) in enumerate(narrow):
    state = event.narrowRoadCameraState
    wide_event = wide_by_id[state.frameId]
    narrow_index = encode_positions['narrowRoadEncodeIdx'][state.frameId]
    wide_index = encode_positions['wideRoadEncodeIdx'][state.frameId]
    if abs(state.timestampSof - wide_event.wideRoadCameraState.timestampSof) > 25_000_000:
      raise ValueError('unpaired camera timestamps')
    calibration = latest('extrinsicsCalibration', event.logMonoTime).extrinsicsCalibration
    meta = latest('drivingModelData', event.logMonoTime).drivingModelData.meta
    pulse, previous = desire_pulse(str(meta.laneChangeState), str(meta.laneChangeDirection), previous)
    counts.update(str(i) for i in np.flatnonzero(pulse))
    # This log has no lateralDelay; match modeld's default zero plus .075 s.
    delay = latest('lateralDelay', event.logMonoTime).lateralDelay.lateralDelay if 'lateralDelay' in groups else 0.
    action = np.array([[float(delay) + .075, float(cp.longitudinalActuatorDelay) + .375]], dtype=np.float32)
    views = []
    for view, frame_index in enumerate([narrow_index, wide_index]):
      transform = get_warp_matrix(np.asarray(calibration.rpyCalib, dtype=np.float32), configs[view].intrinsics,
                                  bool(view)).astype(np.float32)
      views.append(prepares[view](Tensor(readers[view].get(frame_index)), Tensor(transform)).numpy())
    image = np.ascontiguousarray(np.stack(views), dtype=np.uint8)
    if image.shape != (2, 6, 128, 256):
      raise ValueError(f'unexpected image shape {image.shape}')
    destination = args.output / f'{index:06d}.npz'
    np.savez(destination, new_img=image, desire=pulse, traffic_convention=traffic, action_t=action)
    records.append({'index': index, 'source_index': source_index, 'narrow_video_index': narrow_index, 'wide_video_index': wide_index,
                    'frame_id': int(state.frameId), 'capture_ns': int(state.timestampSof),
                    'file': destination.name, 'sha256': digest(destination),
                    'image_sha256': hashlib.sha256(image.tobytes()).hexdigest(),
                    'lane_change_state': str(meta.laneChangeState), 'lane_change_direction': str(meta.laneChangeDirection)})
    if index % 25 == 0:
      print(f'extracted {index + 1}/{args.frames}', flush=True)
  manifest = {'format_version': 2, 'route': '8494c69d3c710e81|000001d4--2648a9a404', 'segment': 4,
              'source_sha256': {f: digest(args.source / f) for f in ['fcamera.hevc', 'ecamera.hevc', 'rlog.zst']},
              'source_cameras': list(camera_key), 'frames': args.frames, 'nominal_hz': 20,
              'preprocessor': 'pinned project examples.openpilot.compile_warp.make_frame_prepare, CPU:LLVM',
              'video_alignment': 'frameId mapped through fullHEVC encode-index segmentId in segment4; camera ordinals are not video indices',
              'conditioning': ('Rising-edge desire reconstructed from latest prior logged lane-change metadata; traffic from driver side; ' +
                               'actuator delay from carParams; lateralDelay defaults to zero only when absent.'),
              'desire_pulse_counts': dict(counts), 'records': records,
              'limits': ('One daytime route; reconstructed conditioning is not original input capture. No inference/state generation here. ' +
                         'Not final calibration coverage or driving quality evidence.')}
  (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
  main()
