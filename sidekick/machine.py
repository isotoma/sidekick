
"""
Tooling for working with a VM that is common accross multiple commands and multiple VM environments.

This is still a grey area of the API and may become part of a base class for the vm module or it might
continue to wrap it.
"""

import os, time

from sidekick import errors
from sidekick.vm.vmware import WorkstationProvider, PlayerProvider
from sidekick.vm.vmware.errors import WRAPPER_WORKSTATION_NOT_INSTALLED, WRAPPER_PLAYER_NOT_INSTALLED

class Machine(object):

    def __init__(self, config):
        self.config = config
        self.vm = None

    def connect(self):
        try:
            p = WorkstationProvider()
            p.connect()
        except WRAPPER_WORKSTATION_NOT_INSTALLED:
            try:
                p = PlayerProvider()
                p.connect()
            except WRAPPER_PLAYER_NOT_INSTALLED:
                raise RuntimeError("Cannot find VM Environment")

        if not os.path.exists(self.config.get("path")):
            print "VM doesnt exit - cloning..."
            base = p.open(self.config.get("base"))
            base.clone(self.config.get("path"))

        self.vm = p.open(self.config.get("path"))

    def approaching(self, desired_state):
        if desired_state == "running":
            if self.vm.get_powerstate() in ("running", "nearly-running", "booting"):
                return True
            return False

    def is_running(self):
        if not self.vm:
            self.connect()
        return self.vm.get_powerstate() == "running"

    def wait_for_boot(self):
        if self.approaching("running"):
            while not self.is_running():
                print "Waiting for boot..."
                time.sleep(5)
        else:
            print self.vm.get_powerstate()

    def power_on(self):
        if not self.vm:
            self.connect()

        if self.is_running():
            raise errors.VmAlreadyRunning()

        self.vm.power_on()
        self.wait_for_boot()

    def provision(self):
        if not self.is_running():
            raise errors.VmNotRunning()

        print "Provisioning vm..."
        print self.vm.get_ip()

        # DO YAYBU STUFF HERE

    def power_off(self):
        if not self.vm:
            self.connect()

        if not self.is_running:
            raise errors.VmNotRunning()

        print "Powering off..."
        self.vm.power_off()

