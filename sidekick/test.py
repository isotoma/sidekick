
from sidekick.vm import vmware
from ctypes import byref

from sidekick.vm.vmware import PlayerProvider, WorkstationProvider, ViServerProvider


def main():
    provider = PlayerProvider()
    #provider = WorkstationProvider()
    #provider = ViServerProvider("https://192.168.201.1:8333/sdk", "root", "hideme")

    provider.connect()

    vm = provider.open("/home/john/vmware/lucid/lucid.vmx")
    vm.power_on()
    vm.power_off()
    vm.release()

    provider.disconnect()

