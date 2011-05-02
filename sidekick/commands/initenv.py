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


from sidekick.commands.base import Command

class InitEnv(Command):

    """ Configure an environment to run nodes in """

    name = "initenv"


    def setup_optparse(self, parser, args):
        args.append("name")

    def do(self):
        if self.environments.contains(self.args[0]):
            raise RuntimeError("That environment is already registered")

        self.environments.register(self.args[0], "fake", {})

