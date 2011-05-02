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
from sidekick.commands.base import Command

class Init(Command):

    """ Generate a Sidekick file in the current directory """

    name = "init"


    def setup_optparse(self, parser, args):
        args.append("name")
        args.append("env")

    def do(self):
        if self.registry.contains(self.args[0]):
            raise RuntimeError("That project is already registered")

        sidekick_file = os.path.abspath("Sidekick")

        self.registry.register(self.args[0], self.args[1], sidekick_file)


