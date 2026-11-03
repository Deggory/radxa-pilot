"""Explicit retrofit identification and C2 platform-name compatibility.

C2 forced "RETROPILOT RETROFIT" in car_helpers and bypassed VIN/FW queries.
Its values.py IDs 0..15 were a placeholder, not a measured CAN signature.
An empty CAN database excludes it from automatic discovery. FW_VERSIONS is
deliberately absent: the modern FW loader must not register an unqualified ECU
database or issue queries for this custom interface.
"""
from opendbc.car.retropilot.values import CAR


FINGERPRINTS = {}

MIGRATION = {
  'RETROPILOT RETROFIT': CAR.RETROPILOT_RETROFIT,
}
