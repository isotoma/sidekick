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

from yaybu.harness.fixture import Fixture


class NodeFixture(Fixture):

    def exists(self, path):
        pass

    def isdir(self, path):
        pass

    def open(self, path, mode='r'):
        return self.console.open(path, mode)

    def touch(self, path):
        with self.open(path, "w") as fp:
            fp.write("")

    def chmod(self, path, mode):
        self.console.chmod(path, mode)

    def readlink(self, path):
         return self.console.readlink(path)

    def symlink(self, source, dest):
        self.console.symlink(source, dest)

    def stat(self, path):
        return self.console.path(path)


