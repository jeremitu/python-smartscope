### see SmartScopeConnect.m
# direct scripting
import clr, os, time, re
from matplotlib import pyplot as plt

for path in [ 
  "",
  "/opt/smartscope/", 
  "c:/Program Files (x86)/LabNation/SmartScope/",
]:
  path += "DeviceInterface.dll"
  if os.path.exists(path):
    #print(path)
    clr.AddReference(path)
    break

from LabNation.DeviceInterface import Devices
from LabNation.DeviceInterface import DataSources

def connection_handler(dev, connected):
    return
    print("connection_handler")
    print(dev)
    print(conected)

if False:
  #problems with callback, why?
  device_manager = Devices.DeviceManager(connection_handler)
  #Devices.DeviceConnectHandler(device_manager.fallbackDevice, True)
else:
  device_manager = Devices.DeviceManager()
print(device_manager)

device_manager.Start(True)

for attempt in range(0, 30):
  time.sleep(0.1)
  #print(attempt)
  if device_manager.SmartScopeConnected: # activeDevice is SmartScope;
    break

scope = device_manager.MainDevice
print(scope)

scope.Running = False
scope.CommitSettings()
assert False == scope.DataSourceScope.IsRunning

scope.DataSourceScope.Start()

# define timebase and trigger position
scope.AcquisitionLength = 0.001
scope.TriggerHoldOff = 0.0005

# set optimal configuration for analog scoping
scope.Rolling = False
scope.SendOverviewBuffer = False
scope.AcquisitionMode = Devices.AcquisitionMode.AUTO
scope.PreferPartial = False
scope.SetViewPort(0, scope.AcquisitionLength)

# define ChannelA input
scope.SetVerticalRange(Devices.AnalogChannel.ChA, -0.5, 0.5)
scope.SetYOffset(Devices.AnalogChannel.ChA, 0)
scope.SetCoupling(Devices.AnalogChannel.ChA, Devices.Coupling.AC)
Devices.AnalogChannel.ChA.SetProbe(Devices.Probe.DefaultX1Probe)

# define ChannelB input
scope.SetVerticalRange(Devices.AnalogChannel.ChB, -3, 3)
scope.SetYOffset(Devices.AnalogChannel.ChB, 0)
scope.SetCoupling(Devices.AnalogChannel.ChB, Devices.Coupling.DC)
Devices.AnalogChannel.ChB.SetProbe(Devices.Probe.DefaultX1Probe)

# define trigger
tv = Devices.TriggerValue()
tv.source = Devices.TriggerSource.Channel
tv.channel = Devices.AnalogChannel.ChA
tv.edge = Devices.TriggerEdge.RISING
tv.level = 0.5
scope.TriggerValue = tv

# go!
#scope.CommitSettings()
scope.Running = True
scope.CommitSettings()

assert True == scope.DataSourceScope.IsRunning

### SmartScopePlot.m
import numpy as np

record = []

def data_handler(data, args):
  # Acquisition, Viewport or Overview
  data_a = data.GetData(DataSources.ChannelDataSourceScope.Viewport, Devices.AnalogChannel.ChA).array
  data_np = np.asarray(data_a)
  assert np.dtype('float32') == data_np.dtype
  record.append(data_np)

scope.DataSourceScope.OnNewDataAvailable += data_handler
scope.DataSourceScope.Start()

time.sleep(2)

scope.DataSourceScope.Stop()

record_np = np.array(record)
print(np.shape(record_np))
if True:
  np.savez('smartscope.npz', analog = record_np)


assert False == scope.DataSourceScope.IsRunning

plt.plot(record[0])
plt.plot(record[1])
plt.show()

device_manager.Stop()
print("finished")
