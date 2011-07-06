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


import sys
import unittest
from testtools.run import TestToolsTestRunner

try:
   from discover import DiscoveringTestLoader as Loader
   has_discover = True
except ImportError:
    from unittest import TestLoader as Loader
    has_discover = False

from sidekick.commands.base import Command


class Test(Command):

    """ Find and run any tests in the current directory """

    name = "test"

    catchbreak = False
    verbosity = 2
    failfast = False
    buffer = False

    def setup_optparse(self, p, a):
        p.add_option("-e", "--environment", action="store", default=None)

    def get_tests(self):
        loader = Loader()
        return loader.discover(".", "test_*.py", None)

    def do(self):
        if self.catchbreak and getattr(unittest, 'installHandler', None):
            unittest.installHandler()

        runner = TestToolsTestRunner(sys.stdout)
        results = runner.run(self.get_tests())

        sys.exit(not results.wasSuccessful())

