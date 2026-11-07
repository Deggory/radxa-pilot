# Source-audit replay only; never reads or writes a device. Python standard library.
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
import subprocess
import xml.etree.ElementTree as E

parser = argparse.ArgumentParser(
  description='Replay selected Ocelot power nets; source audit, not EDA/ERC or hardware qualification'
)
parser.add_argument('--workspace', type=Path, required=True)
args = parser.parse_args()
W = args.workspace.resolve()
p = W / 'ocelot/hardware/ocelot-pro/ocelot-pro_schematic.schdoc'
records = [
  dict(t.split('=', 1) for t in line.strip('|').split('|') if '=' in t)
  for line in p.read_text(encoding='utf-8-sig').splitlines()[1:]
]


# EasyEDA-export fractional offsets (e.g. 280.01 versus wire280) are normalized
# to0.1 schematic unit for this selected trace, then checked against the original PDF.
def coord(r, k):
  raw = int(r.get(k, '0')) * 100000 + int(r.get(k + '_FRAC', '0'))
  return round(raw / 10000) * 10000


def xy(r):
  return coord(r, 'LOCATION.X'), coord(r, 'LOCATION.Y')


parts = {int(r['OWNERINDEX']): r['TEXT'] for r in records if r.get('RECORD') == '34'}


def endpoint(r):
  x, y = xy(r)
  dx, dy = ((1, 0), (0, 1), (-1, 0), (0, -1))[int(r.get('PINCONGLOMERATE', '0')) & 3]
  length = int(r.get('PINLENGTH', '0')) * 100000
  return x + dx * length, y + dy * length


pins = [
  {
    'part': parts.get(int(r.get('OWNERINDEX', '-1')), '?'),
    'pin': r.get('NAME'),
    'pad': r.get('DESIGNATOR'),
    'point': endpoint(r),
  }
  for r in records
  if r.get('RECORD') == '2'
]
labels = [(xy(r), r['TEXT']) for r in records if r.get('RECORD') in ('17', '25') and r.get('TEXT')]
segments = []
for r in records:
  if r.get('RECORD') == '27':
    pts = [(coord(r, f'X{i}'), coord(r, f'Y{i}')) for i in range(1, int(r['LOCATIONCOUNT']) + 1)]
    segments.extend(zip(pts, pts[1:], strict=False))
nodes = {p['point'] for p in pins} | {point for point, label in labels} | {p for seg in segments for p in seg}
parent = {p: p for p in nodes}


def find(p):
  while parent[p] != p:
    parent[p] = parent[parent[p]]
    p = parent[p]
  return p


def union(a, b):
  parent[find(a)] = find(b)


for a, b in segments:
  points = [
    p
    for p in nodes
    if (b[0] - a[0]) * (p[1] - a[1]) == (b[1] - a[1]) * (p[0] - a[0])
    and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
    and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
  ]
  for point in points:
    union(a, point)
# Named nets/power symbols join repeated labels; crossings without nodes aren't joined.
by_name = defaultdict(list)
for point, label in labels:
  by_name[label].append(point)
for points in by_name.values():
  for point in points[1:]:
    union(points[0], point)
groups = defaultdict(lambda: {'labels': set(), 'pins': []})
for pin in pins:
  groups[find(pin['point'])]['pins'].append({k: v for k, v in pin.items() if k != 'point'})
for point, label in labels:
  groups[find(point)]['labels'].add(label)
selected = []
for group in groups.values():
  if (
    any(p['part'] == 'USB1' and p['pin'] == 'VBUS' for p in group['pins'])
    or any(p['part'] == 'U1' and p['pin'] in ['PA9', 'PA11', 'PA12'] for p in group['pins'])
    or group['labels']
    & {
      '5V',
      '3.3V',
      '12V',
      'CAN1_EN',
      'CAN2_EN',
      'CAN3_EN',
      'CAN1_RX',
      'CAN1_TX',
      'CAN2_RX',
      'CAN2_TX',
      'CAN3_RX',
      'CAN3_TX',
      'IGN_SIM',
    }
  ):
    selected.append({'labels': sorted(group['labels']), 'pins': group['pins']})
result = {
  'source': str(p.relative_to(W)),
  'records': len(records),
  'wire_segments': len(segments),
  'pins': len(pins),
  'nodes': len(nodes),
  'selected_nets': selected,
  'coordinate_normalization': ('0.1schematic-unit grid for fractional export offsets; selected paths visually checked ' +
    'against original PDF, not native EDA validation'),
  'limits': 'Selected axis-aligned ASCII wire/label connectivity; not a full EDA/ERC or board equivalence proof. Original PDF also visually checked.',
}
pro = result

checks = []


def checked(name, condition):
  if not condition:
    raise ValueError(name)
  checks.append(name)


base = W / 'ocelot/hardware/ocelot-gateway'
schematic = E.parse(base / 'ocelot-gw.sch').getroot().find('.//schematic')
board = E.parse(base / 'ocelot-gw.brd').getroot().find('.//board')
parts = {p.get('name'): p.attrib for p in schematic.findall('./parts/part')}
nets = {n.get('name'): [r.attrib for r in n.findall('.//pinref')] for n in schematic.findall('./sheets/sheet/nets/net')}
board_nets = {
  n.get('name'): {(c.get('element'), c.get('pad')) for c in n.findall('contactref')}
  for n in board.findall('./signals/signal')
}
board_parts = {p.get('name') for p in board.findall('./elements/element')}


def pads(ref):
  part = parts[ref['part']]
  library = schematic.find("./libraries/library[@name='" + part['library'] + "']")
  device = library.find(
    "./devicesets/deviceset[@name='" + part['deviceset'] + "']/devices/device[@name='" + part['device'] + "']"
  )
  return {
    (ref['part'], pad)
    for c in device.findall('./connects/connect')
    if c.get('gate') == ref['gate'] and c.get('pin') == ref['pin']
    for pad in c.get('pad').split()
  }


selected_names = [
  'N$5',
  '5V',
  '3.3V',
  '12V',
  'N$3',
  'N$4',
  'N$10',
  'N$11',
  'CAN1_RX',
  'CAN1_TX',
  'CAN2_RX',
  'CAN2_TX',
  'CAN3_RX',
  'CAN3_TX',
  'CAN1_EN',
  'CAN2_EN',
  'CAN3_EN',
]
gateway_nets = []
for name in selected_names:
  physical = set().union(*(pads(r) for r in nets[name] if r['part'] in board_parts))
  checked('Gateway schematic/board pad equality: ' + name, physical == board_nets[name])
  gateway_nets.append(
    {'name': name, 'logical_pins': nets[name], 'board_pads': [{'part': p, 'pad': q} for p, q in sorted(physical)]}
  )
checked(
  'Gateway PA9 has no schematic net',
  not any(r['part'] == 'U1' and r['pin'] == 'PA9' for refs in nets.values() for r in refs),
)
checked('Gateway U1 pad42 has no board signal', not any(('U1', '42') in refs for refs in board_nets.values()))
checked(
  'Gateway USB VBUS net only J1 VBUS / D1 anode',
  {(r['part'], r['pin']) for r in nets['N$5']} == {('J1', 'VBUS'), ('D1', 'A')},
)
checked('Gateway BAS40 diode', parts['D1']['deviceset'] == 'BAS40')
checked(
  'Gateway MIC5233 regulators',
  parts['PS1']['deviceset'] == 'MIC5233-5.0YM5-TR' and parts['IC1']['deviceset'] == 'MIC5233-3.3YM5-TR',
)


def pro_net(part, pin):
  return next(n for n in pro['selected_nets'] if any(p['part'] == part and p['pin'] == pin for p in n['pins']))


def pairs(net):
  return {(p['part'], p['pin']) for p in net['pins']}


checked(
  'Pro USB VBUS only USB1/D3 anode',
  pairs(pro_net('USB1', 'VBUS')) == {('USB1', 'VBUS'), ('D3', 'A')} and len(pro_net('USB1', 'VBUS')['pins']) == 3,
)
checked(
  'Pro shared5V joins diode/regulator rails',
  {('D3', 'K'), ('PS1', 'OUT'), ('PS2', 'IN'), ('PS2', 'EN')} <= pairs(pro_net('D3', 'K'))
  and pro_net('D3', 'K')['labels'] == ['5V'],
)
checked('Pro PA9 only U1/header H5 pin9', pairs(pro_net('U1', 'PA9')) == {('U1', 'PA9'), ('H5', '9')})
expected = {
  'CAN1_RX': 'PB8',
  'CAN1_TX': 'PB9',
  'CAN2_RX': 'PB5',
  'CAN2_TX': 'PB6',
  'CAN3_RX': 'PA8',
  'CAN3_TX': 'PA15',
  'CAN1_EN': 'PC1',
  'CAN2_EN': 'PC13',
  'CAN3_EN': 'PA0',
}
for label, pin in expected.items():
  checked(
    'Both base drawings CAN pin: ' + label,
    any(r['part'] == 'U1' and r['pin'] == pin for r in nets[label])
    and any(label in g['labels'] and ('U1', pin) in pairs(g) for g in pro['selected_nets']),
  )
usb = (W / 'ocelot/firmware/chimera/usb.h').read_text()
checked(
  'Legacy F4 sets both session override bits',
  'USBx->GOTGCTL |= USB_OTG_GOTGCTL_BVALOVAL;' in usb and 'USBx->GOTGCTL |= USB_OTG_GOTGCTL_BVALOEN;' in usb,
)
checked('Legacy descriptor raw power bytes', '0xc0, 0x32, // Attributes, Max Power' in usb)
files = [
  'ocelot/hardware/ocelot-gateway/ocelot-gw.sch',
  'ocelot/hardware/ocelot-gateway/ocelot-gw.brd',
  'ocelot/hardware/ocelot-pro/ocelot-pro_schematic.schdoc',
  'ocelot/hardware/ocelot-pro/ocelot-pro-schematic.pdf',
  'ocelot/firmware/chimera/usb.h',
  'ocelot/firmware/boards/common.h',
  'ocelot/firmware/SConscript',
]
result = {
  'date': '2026-11-07',
  'scope': 'T01b base power schematic trace; no firmware or device change',
  'owner_clarification': {
    'quote': 'see on ovelot foldeer the sch is same onli i/o is added',
    'meaning': 'Owner identifies Ocelot schematic as Chimera base circuit with added IO; use as working design baseline, not a measured board test',
  },
  'ocelot_head': subprocess.check_output(['git', '-C', str(W / 'ocelot'), 'rev-parse', 'HEAD'], text=True).strip(),
  'sources_sha256': {p: hashlib.sha256((W / p).read_bytes()).hexdigest() for p in files},
  'gateway': {
    'parts': len(parts),
    'nets': len(nets),
    'selected_nets': gateway_nets,
    'pa9': 'No net in schematic or board pad42',
  },
  'pro': pro,
  'can_map': expected,
  'legacy_usb': {
    'f4_session': 'BVALOEN + BVALOVAL forced; VBDEN line commented',
    'descriptor_attributes_byte': '0xc0',
    'descriptor_max_power_byte': '0x32',
    'meaning': 'Historical software declarations, not measurements or a selected new profile',
  },
  'checks': checks,
  'limits': [
    'Owner-supplied base-circuit applicability, not independently measured Chimera revision equivalence',
    'Pro trace uses normalized0.1unit coordinates and visual original-PDF check; not native EDA/ERC',
    'No transceiver/regulator current, reverse-current, thermal, USB compliance or installed recovery qualification',
    'Existing supervisor requires an actual detector; these base drawings provide none. No fabricated PRESENT callback or PA9 reassignment',
    'No firmware/host/flash/device/config/TX/relay/OBD-C changes',
  ],
  'next': ('Specify and implement an explicit source-backed legacy no-VBUS session mode offline, ' +
    'separate from sensed mode; actual attachment and bench/recovery qualification remain pending'),
}
print(json.dumps(result, indent=2))
