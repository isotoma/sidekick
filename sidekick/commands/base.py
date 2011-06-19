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


import os, sys, optparse

from sidekick.errors import SidekickError
from sidekick.cluster import Cluster
from sidekick.registry import Instances, Environments
from sidekick.vm import ProviderType

class CommandType(type):

    commands = {}

    def __new__(meta, class_name, bases, new_attrs):
        cls = type.__new__(meta, class_name, bases, new_attrs)

        command = new_attrs.get("name", None)
        id = (cls.parent, command)

        if command:
            if id in meta.commands:
                raise SidekickError("Command '%s' was already defined")
            meta.commands[id] = cls

        return cls


class BaseCommand(object):

    __metaclass__ = CommandType
    parent = None

    def __init__(self, args):
        raise NotImplementedError(self.__init__)

    def do(self):
        raise NotImplementedError(self.do)


class NamespaceCommand(BaseCommand):

    def __init__(self, args):
        self.args = args

    def get_children(self):
        for command in CommandType.commands.values():
            if command.parent != self.__class__:
                continue
            yield command

    def usage(self):
        print "Usage: %s SUBCOMMAND [OPTIONS]" % sys.argv[0]

        children = list(self.get_children())
        if children:
            maxpad = max(len(c.name) for c in children) + 4

            print ""
            for c in children:
                pad = " " * (maxpad - len(c.name))
                print "    %s%s%s" % (c.name, pad, c.__doc__.split("\n")[0])
            print ""

    def do(self):
        if len(self.args) == 0:
            self.usage()
            return

        cmd = self.args[0]
        args = self.args[1:]

        id = (self.__class__, cmd)

        if id not in CommandType.commands:
            self.usage()
            return

        c = CommandType.commands[id]
        c(args).do()


class RootNamespace(NamespaceCommand):
    pass


class Command(BaseCommand):

    parent = RootNamespace

    def __init__(self, args):
        self.cluster = None
        self.sidekick_file = None

        p = optparse.OptionParser()

        # Set default optparse settings
        p.prog = " ".join((sys.argv[0], self.name))
        p.description = self.__doc__

        # Allow subclass to define its own options
        expected_args = []
        self.setup_optparse(p, expected_args)

        p.usage = " ".join(["%prog", "[options]"] + expected_args)

        self.options, self.args = p.parse_args(args)

        if len(self.args) != len(expected_args):
            print p.error("Expected %d arguments, but got %d" % (len(expected_args), len(self.args)))

        self.environments = Environments(defaults_fn=ProviderType.get_defaults)
        self.registry = Instances()

    def setup_optparse(self, p, a):
        pass

    def get_environment(self, name):
        env = self.environments.get(name)
        return ProviderType.providers[env['type']](env)

    def get_environments(self):
        for env in self.environments.all():
            yield self.get_environment(env)

    def get_current_cluster(self):
        if self.options.cluster:
            return self.get_cluster(self.options.cluster)

        path = ["/"] + list(os.getcwd().split(os.path.sep)) + ["Sidekick"]
        while path and not os.path.exists(os.path.join(*path)):
            path = path[:-2] + ["Sidekick"]

        if not os.path.exists(os.path.join(*path)):
            raise SidekickError("You did not specify a cluster and there is no Sidekick in cwd to look one up")

        for cluster in self.get_clusters():
            if cluster.config['sidekick-file'] == os.path.join(*path):
                return cluster

        raise SidekickError("You failed to specify a cluster and one could not be found based on cwd.")

    def get_cluster(self, name):
        cluster = self.registry.get(name)
        return Cluster(
            cluster['name'],
            self.get_environment(cluster['env']),
            cluster)

    def get_clusters(self):
        for cluster in self.registry.all():
            yield self.get_cluster(cluster)


class ProjectCommand(Command):

    """ A command that access project information from the Sidekick file """

    def __init__(self, args):
        super(ProjectCommand, self).__init__(args)

    def setup_optparse(self, parser, args):
        parser.add_option("-c", "--cluster")
