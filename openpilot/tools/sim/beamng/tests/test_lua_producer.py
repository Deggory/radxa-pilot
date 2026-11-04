from pathlib import Path
import unittest

from lupa.lua54 import LuaRuntime
from cffi import FFI

from openpilot.tools.sim.beamng.pc.gateway import FLOAT_FIELDS, PACKET, Sample


class TestLuaProducer(unittest.TestCase):
  def setUp(self):
    self.lua = LuaRuntime(unpack_returned_tuples=True)
    self.lua.execute('''
      now=100
      package.preload.socket=function() return {gettime=function() return now end} end
      obj={getID=function() return 12 end,
           getRollPitchYawAngularVelocity=function() return 0.1,-0.2,0.3 end}
      electrics={values={wheelspeed=10,steering=-12.3,rpm=1200,throttle_input=0.25,
                        brake_input=0.1,brake=0.3,ignitionLevel=2,gearIndex=3}}
      sensors={ffiSensors={sensorX=-1.2,sensorY=2.3,sensorZ=0}}
      wheels={wheels={{name='FL',angularVelocity=-20,radius=0.5},
                      {name='FR',angularVelocity=21,radius=0.5},
                      {name='RL',angularVelocity=-19,radius=0.5},
                      {name='RR',angularVelocity=22,radius=0.5}}}
      extensions={cruiseControl={getConfiguration=function() return {isEnabled=false,targetSpeed=20} end}}
    ''')
    path=Path(__file__).resolve().parents[1]/'pc/mod/lua/vehicle/protocols/radxaRetropilot.lua'
    self.module = self.lua.execute(path.read_text())
    self.module.init()

  def collect(self):
    out = self.lua.table()
    self.module.fillStruct(out,0.02)
    values = [int(out.session), out.wall_time, out.sim_time, int(out.sequence), int(out.valid)]
    return Sample.decode(PACKET.pack(out.format.encode(), *values, *[out[name] for name in FLOAT_FIELDS],int(out.buttons)))

  def test_actual_lua_values_and_optional_availability(self):
    result = self.collect()
    self.assertEqual(result.speed,10)
    self.assertAlmostEqual(result.angle,-12.3,places=4)
    self.assertAlmostEqual(result.accel_x,1.2,places=5)
    self.assertEqual(result.wheel_rl,9.5)
    self.assertAlmostEqual(result.brake_input,0.1,places=5)
    self.assertAlmostEqual(result.brake,0.3,places=5)
    self.assertTrue(result.valid & (1 << 11))
    self.assertFalse(result.valid & (1 << 12))  # buttons are not inferred from cruise state
    self.lua.execute('extensions.cruiseControl=nil; sensors.ffiSensors=0; wheels.wheels[1].radius=nil')
    result=self.collect()
    self.assertFalse(result.valid & (1 << 8 | 1 << 10 | 1 << 11))

  def test_reset_changes_session_and_time(self):
    first=self.collect()
    self.lua.execute('now=100.01')
    self.module.reset()
    second=self.collect()
    self.assertNotEqual(first.session,second.session)
    self.assertAlmostEqual(second.sim_time,0.02)

  def test_ffi_layout_and_missing_not_zero_valid(self):
    ffi=FFI()
    ffi.cdef('typedef struct {'+self.module.getStructDefinition()+'} Telemetry;')
    self.assertEqual(ffi.sizeof('Telemetry'),PACKET.size)
    self.assertEqual(ffi.offsetof('Telemetry','wall_time'),8)
    self.assertEqual(ffi.offsetof('Telemetry','buttons'),PACKET.size-8)
    self.lua.execute('electrics.values.steering=nil; electrics.values.brake_input=nil')
    result=self.collect()
    self.assertFalse(result.valid & (1 << 1 | 1 << 5))


if __name__=='__main__':
  unittest.main()
