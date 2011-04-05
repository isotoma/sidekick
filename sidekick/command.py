
import sys, optparse

from sidekick.registry import Registry
from sidekick.project import Project


class CommandType(type):

    commands = {}

    def __new__(meta, class_name, bases, new_attrs):
        cls = type.__new__(meta, class_name, bases, new_attrs)

        command = new_attrs.get("name", None)
        if command:
            if command in meta.commands:
                raise RuntimeError("Command '%s' was already defined")
            meta.commands[command] = cls

        return cls


class Command(object):

    __metaclass__ = CommandType

    def __init__(self, args):
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

        self.registry = Registry()

    def setup_optparse(self, p, a):
        pass

    def do(self):
        raise NotImplementedError


class ProjectCommand(Command):

    """ A command that access project information from the Sidekick file """

    def __init__(self, args):
        super(ProjectCommand, self).__init__(args)
        self.project = Project()

