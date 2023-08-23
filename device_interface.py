import clr
import os
from time import sleep

class DeviceInterface:
    Devices = None
    DataSources = None
    enums = None
    device_manager = None

    def __init__(self, dll_path = ""):
        for path in [ 
          dll_path,
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

        self.Devices = Devices
        self.DataSources = DataSources

        self.device_manager = self.Devices.DeviceManager()
        self.device_manager.Start()

    def __del__(self):
        self.device_manager.Stop()

    def wait_for_real_device(self):
        while not self.device_manager.SmartScopeConnected:
            sleep(0.1)

