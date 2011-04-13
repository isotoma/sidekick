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


import os

import yay

from sidekick.errors import NoProjectFile
from sidekick.machine import Machine

class Project(object):

    def __init__(self):
        if not os.path.exists("Sidekick"):
            raise NoProjectFile("No project information exists, run sidekick init?")

        self.config = yay.load_uri("Sidekick")

    def all_vms(self):
        for vm in self.config.get("environments", []):
            yield Machine(self, vm)

