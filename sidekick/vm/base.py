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

from sidekick.provisioners import ProvisionerType
from sidekick.console import Console
from sidekick.errors import SidekickError


class ProviderType(type):

    providers = {}

    def __new__(meta, class_name, bases, attrs):
        cls = type.__new__(meta, class_name, bases, attrs)

        if "name" in attrs:
            if attrs["name"] in meta.providers:
                raise SidekickError("Provider '%s' already defined" % attrs['name'])

            meta.providers[attrs["name"]] = cls

        return cls

    @classmethod
    def get_defaults(cls):
        defaults = {}
        for p in cls.providers.values():
            defaults.update(p.get_defaults())
        return defaults


class BaseProvider(object):

    __metaclass__ = ProviderType

    @classmethod
    def get_defaults(self):
        return {}


class BaseMachine(object):

    def __init__(self, config):
        self.config = config

    @property
    def console(self):
        return Console(self)

    def provision(self):
        #if not self.is_running():
        #    raise errors.VmNotRunning()

        print "Provisioning vm..."

        p = None
        if "provisioner" in self.config:
            try:
                p = ProvisionerType.provisioners[self.config["provisioner"]]
            except KeyError:
                raise SidekickError("There is no such provisioner: '%s'" % self.config["provisioner"])
        else:
            for p in ProvisionerType.provisioners.values():
                if p.can_provision(self):
                    break
            else:
                raise SidekickError("Cannot find a suitable provisioner")

        # Actually do this thing
        p(self).provision()


