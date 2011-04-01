
"""
Tooling for working with a VM that is common accross multiple commands and multiple VM environments.

This is still a grey area of the API and may become part of a base class for the vm module or it might
continue to wrap it.
"""

from sidekick.vm.vmware import WorkstationProvider, PlayerProvider
from sidekick.vm.vmware.errors import WRAPPER_WORKSTATION_NOT_INSTALLED, WRAPPER_PLAYER_NOT_INSTALLED

class Machine(object):

    def __init__(self, config):
        self.config = config

    def start(self):
        try:
            p = WorkstationProvider()
            p.connect()
        except WRAPPER_WORKSTATION_NOT_INSTALLED:
            try:
                p = PlayerProvider()
                p.connect()
            except WRAPPER_PLAYER_NOT_INSTALLED:
                raise RuntimeError("Cannot find VM Environment")

        vm = p.open(self.config.get("path"))

