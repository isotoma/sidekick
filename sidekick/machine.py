# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Tooling for working with a VM that is common accross multiple commands and multiple VM environments.

This is still a grey area of the API and may become part of a base class for the vm module or it might
continue to wrap it.
"""

import os

from sidekick import errors
#from sidekick.vm.vmware import WorkstationProvider, PlayerProvider
#from sidekick.vm.vmware.errors import WRAPPER_WORKSTATION_NOT_INSTALLED, WRAPPER_PLAYER_NOT_INSTALLED
from sidekick.vm import ProviderType
from sidekick.provisioners import ProvisionerType


class Machine(object):

    def __init__(self, project, config):
        self.project = project
        self.config = config

        providers = ProviderType.find(project, config)
        if len(providers) != 1:
            raise RuntimeError("Was hoping for 1 provider, got %d" % len(providers))

        self.vm = providers[0]().provide(self)

    @property
    def base(self):
        return self.config["base"]

    @property
    def name(self):
        return self.config["name"]

    def is_running(self):
        return self.vm.get_powerstate() == "running"

    def get_ip(self):
        return self.vm.get_ip()

    def power_on(self):
        if self.is_running():
            raise errors.VmAlreadyRunning()

        self.vm.power_on()

    def provision(self):
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
        if not self.is_running:
            raise errors.VmNotRunning()

        print "Powering off..."
        self.vm.power_off()

