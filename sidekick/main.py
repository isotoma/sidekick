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

import sys, optparse, os, logging

from sidekick.errors import SidekickError
from sidekick.commands import RootNamespace

def main():
    logging.basicConfig(format="%(message)s", level=logging.ERROR)

    root = logging.getLogger("sidekick")
    root.setLevel(logging.DEBUG)

    cmd = RootNamespace(sys.argv[1:])
    try:
        rv = cmd.do()
    except SidekickError, e:
        print e.args[0]
        sys.exit(1)

    print "done."
    sys.exit(rv)

