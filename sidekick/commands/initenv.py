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

from sidekick.errors import SidekickError
from sidekick.commands.base import RootNamespace, NamespaceCommand, Command


class Environment(NamespaceCommand):

    """ Commands for managing node environments """

    name = "env"
    parent = RootNamespace


class Define(Command):

    """ Configure an environment to run nodes in """

    name = "define"
    parent = Environment

    def setup_optparse(self, parser, args):
        parser.add_option("-p", "--provider")
        args.append("name")

    def do(self):
        if self.environments.contains(self.args[0]):
            raise SidekickError("That environment is already registered")

        self.environments.register(self.args[0], self.options.provider, {})


class List(Command):

    """ List configured environments """

    name = "list"
    parent = Environment

    def do(self):
        envs = self.environments.all()

        if len(envs) == 0:
            print "There are no defined environments."

        print "The following environments are defined:"
        print ""

        for name in self.environments.all():
            env = self.environments.get(name)

            print "    %s (provider=%s)" % (name, env["type"])

        print ""


class Delete(Command):

    """ Delete an environment """

    name = "delete"
    parent = Environment

    def setup_optparse(self, parser, args):
        args.append("ENVIRONMENT")

    def do(self):
        if not self.args[0] in self.environments.all():
            raise SidekickError("No such environment '%s'" % self.args[0])

        self.environments.delete(self.args[0])

