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

from sidekick.vm import BaseProvider, BaseMachine


class Provider(BaseProvider):

    name = "fake"
    parameters = [
    ]

    style = None

    def __init__(self, config):
        self.config = config

    def provide(self, machine):
        return VirtualMachine(self)


class VirtualMachine(BaseMachine):

    def __init__(self, provider, machine):
        self.provider = provider

    def get_ip(self):
        return "127.0.0.1"

    def get_powerstate(self):
        return "running"

    def power_on(self):
        pass

    def get_ssh_details(self):
        return "sidekick", "127.0.0.1", "22"

    def power_off(self):
        pass

    def clone(self, path):
        pass

    def release(self):
        pass


