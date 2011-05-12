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
Main entry point. Finds a Command object and hands control over to it.
"""

import sys, optparse, os

from sidekick.errors import SidekickError
from sidekick.commands import CommandType

def usage():
    print "Usage: %s SUBCOMMAND [OPTIONS]" % sys.argv[0]

    max_padding = max(len(name) for name in CommandType.commands.keys()) + 4
    if max_padding > 4:
        print ""
        for name, command in CommandType.commands.items():
            padding = " " * (max_padding - len(name))
            print "    %s%s%s" % (name, padding, command.__doc__.split("\n")[0])
        print ""



def main():
    args = sys.argv[1:]

    if len(args) == 0:
        usage()
        sys.exit(1)

    command = args[0]
    if not command in CommandType.commands:
        print "Unknown subcommand; %s" % command
        sys.exit(1)

    cmd = CommandType.commands[command](args[1:])

    try:
        cmd.do()
    except SidekickError, e:
        print e.args[0]
        sys.exit(1)

    print "done."

