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


from sidekick.provisioners.base import Provisioner

class ShellProvisioner(Provisioner):

    name = "shell"

    @staticmethod
    def can_provision(machine):
        if "script" in machine.config:
            return True

    def provision(self):
        with self.machine.console as c:
            c.run_script(self.machine.config("script"))

