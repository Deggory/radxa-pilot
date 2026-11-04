-- SPDX-License-Identifier: bCDDL-1.1
-- Uses the documented BeamNG protocol API and the installed motionSim conventions.
-- Read-only: no input events, throttle overrides, cruise changes or camera changes.
local M = {}
local net = require('socket')
local session, sequence, simTime, lastAngle, lastAngleTime

local function finite(value)
  return type(value) == 'number' and value == value and math.abs(value) ~= math.huge
end

local function reset()
  session = math.floor(net.gettime() * 1000000 + obj:getID()) % 4294967295
  sequence, simTime, lastAngle, lastAngleTime = 0, 0, nil, nil
end

local function getStructDefinition()
  return [[
    char format[4];
    unsigned int session;
    double wall_time;
    double sim_time;
    unsigned int sequence;
    unsigned int valid;
    float speed, angle, rate, rpm, throttle, brake_input, brake, ignition, gear;
    float accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z;
    float wheel_fl, wheel_fr, wheel_rl, wheel_rr;
    float cruise_available, cruise_enabled, cruise_speed;
    unsigned int buttons;
  ]]
end

local function fillStruct(o, dtSim)
  -- The protocol manager clears its FFI packet before this call.
  sequence = sequence + 1
  if finite(dtSim) and dtSim > 0 then simTime = simTime + dtSim end
  o.format, o.session, o.sequence = 'RPT1', session, sequence
  o.wall_time, o.sim_time, o.valid, o.buttons = net.gettime(), simTime, 0, 0
  -- Explicit initialization also allows the source to be tested with a plain Lua table.
  local names = {'speed','angle','rate','rpm','throttle','brake_input','brake','ignition','gear',
    'accel_x','accel_y','accel_z','gyro_x','gyro_y','gyro_z','wheel_fl','wheel_fr','wheel_rl','wheel_rr',
    'cruise_available','cruise_enabled','cruise_speed'}
  for _, name in ipairs(names) do o[name] = 0 end
  local function mark(bit) o.valid = o.valid + 2^bit end
  local function assign(name, value, bit)
    if finite(value) then o[name] = value; mark(bit); return true end
    return false
  end
  local e = electrics.values
  assign('speed', finite(e.wheelspeed) and math.abs(e.wheelspeed) or nil, 0)
  if assign('angle', e.steering, 1) then
    if lastAngle and lastAngleTime and simTime > lastAngleTime then
      assign('rate', (e.steering-lastAngle)/(simTime-lastAngleTime), 13)
    end
    lastAngle, lastAngleTime = e.steering, simTime
  else
    lastAngle, lastAngleTime = nil, nil
  end
  if finite(e.ignitionLevel) then assign('ignition', e.ignitionLevel > 0 and 1 or 0, 2) end
  assign('rpm', e.rpm, 3)
  -- Preserve the driver input independently of applied/overridden pedal state.
  assign('throttle', e.throttle_input, 4)
  assign('brake_input', e.brake_input, 5)
  assign('brake', e.brake, 6)
  assign('gear', e.gearIndex, 7)

  -- Same components/units as shipped motionSim/protocols.lua, without smoothing.
  -- sensorZ (inertial) is intentionally used, not sensorZnonInertial with gravity.
  local sensorOK, sx, sy, sz = pcall(function()
    local s = sensors.ffiSensors
    return s.sensorX, s.sensorY, s.sensorZ
  end)
  if sensorOK and finite(sx) and finite(sy) and finite(sz) then
    o.accel_x, o.accel_y, o.accel_z = -sx, -sy, -sz
    mark(8)
  end
  local ok, roll, pitch, yaw = pcall(obj.getRollPitchYawAngularVelocity, obj)
  if ok and finite(roll) and finite(pitch) and finite(yaw) then
    o.gyro_x, o.gyro_y, o.gyro_z = roll, pitch, yaw
    mark(9)
  end
  -- Each wheel uses its own measured angular velocity and nominal rolling radius.
  -- These are kinematic speed magnitudes, not a copy of scalar vehicle speed.
  local found = {}
  for _, wheel in pairs((wheels and wheels.wheels) or {}) do
    local name = type(wheel.name) == 'string' and string.lower(wheel.name) or ''
    if name == 'fl' or name == 'fr' or name == 'rl' or name == 'rr' then
      if finite(wheel.angularVelocity) and finite(wheel.radius) and wheel.radius > 0 then
        found[name] = math.abs(wheel.angularVelocity) * wheel.radius
      end
    end
  end
  if found.fl and found.fr and found.rl and found.rr then
    o.wheel_fl, o.wheel_fr, o.wheel_rl, o.wheel_rr = found.fl, found.fr, found.rl, found.rr
    mark(10)
  end
  local cruise = extensions.cruiseControl
  if cruise and type(cruise.getConfiguration) == 'function' then
    local success, config = pcall(cruise.getConfiguration)
    if success and type(config) == 'table' and type(config.isEnabled) == 'boolean' and finite(config.targetSpeed) then
      o.cruise_available, o.cruise_enabled, o.cruise_speed = 1, config.isEnabled and 1 or 0, config.targetSpeed
      mark(11)
    end
  end
  -- There is no evidenced generic cruise-button-state API. Bit12 stays clear;
  -- enabled/set-speed state above must never be turned into invented button edges.
end

M.init = reset
M.reset = reset
M.getAddress = function() return '127.0.0.1' end
M.getPort = function() return 49160 end
M.getMaxUpdateRate = function() return 50 end
M.isPhysicsStepUsed = function() return true end
M.getStructDefinition = getStructDefinition
M.fillStruct = fillStruct
return M
