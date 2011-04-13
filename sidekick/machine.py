
"""
Tooling for working with a VM that is common accross multiple commands and multiple VM environments.

This is still a grey area of the API and may become part of a base class for the vm module or it might
continue to wrap it.
"""

import os, time

from sidekick import errors
#from sidekick.vm.vmware import WorkstationProvider, PlayerProvider
#from sidekick.vm.vmware.errors import WRAPPER_WORKSTATION_NOT_INSTALLED, WRAPPER_PLAYER_NOT_INSTALLED
from sidekick.vm import ProviderType
from sidekick.provisioners import ProvisionerType


class Machine(object):

    def __init__(self, project, config):
        self.project = project
        self.config = config

        providers = ProviderType.find(project)
        if len(providers) != 1:
            raise RuntimeError("Was hoping for 1 provider, got %d" % len(providers))

        self.vm = providers[0].provide()

        #try:
        #    p = WorkstationProvider()
        #    p.connect()
        #except WRAPPER_WORKSTATION_NOT_INSTALLED:
        #    try:
        #        p = PlayerProvider()
        #        p.connect()
        #    except WRAPPER_PLAYER_NOT_INSTALLED:
        #        raise RuntimeError("Cannot find VM Environment")

        #if not os.path.exists(self.config.get("path")):
        #    print "VM doesnt exit - cloning..."
        #    base = p.open(self.config.get("base"))
        #    base.clone(self.config.get("path"))

        #self.vm = p.open(self.config.get("path"))

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

    def wait_for_ip(self):
        ip = None
        while not ip:
            print "Waiting for ip..."
            ip = self.vm.get_ip()
            time.sleep(5)
        return ip

    def get_ip(self):
        if not self.vm:
            self.connect()
        return self.vm.get_ip()

    def power_on(self):
        if not self.vm:
            self.connect()

        if self.is_running():
            raise errors.VmAlreadyRunning()

        self.vm.power_on()
        self.wait_for_boot()
        self.wait_for_ip()

    def provision(self):
        if not self.vm:
            self.connect()

        #if not self.is_running():
        #    raise errors.VmNotRunning()

        print "Provisioning vm..."

        p = None
        if "provisioner" in self.project.config:
            try:
                p = ProvisionerType.provisioners[self.project.config["provisioner"]]
            except KeyError:
                raise RuntimeError("There is no such provisioner: '%s'" % self.project.config["provisioner"])
        else:
            for p in ProvisionerType.provisioners.values():
                if p.can_provision(self):
                    break
            else:
                raise RuntimeError("Cannot find a suitable provisioner")

        # Actually do this thing
        p(self).provision()

    def power_off(self):
        if not self.vm:
            self.connect()

        if not self.is_running:
            raise errors.VmNotRunning()

        print "Powering off..."
        self.vm.power_off()

