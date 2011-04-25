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
The registry is a user wide map of all known projects and environments.

It's purpose is to be able to enumerate any active environments even if
you don't remember what you left on, or worst.. you lost your Sidekick
file.
"""

import os
import yay

class Registry(object):

    def __init__(self):
        self.environments = {}

        self.dotdir = os.path.expanduser("~/.sidekick")
        self.registry = os.path.join(self.dotdir, "registry")
        self.index_file = os.path.join(self.registry, "index.yay")

        if not os.path.exists(self.registry):
            os.makedirs(self.registry)

        if os.path.exists(self.index_file):
            self.index = yay.load_uri(self.index_file)
        else:
            self.index = {}

    def save(self):
        open(self.index_file, "w").write(yay.dump(self.index))

    def contains(self, name):
        return name in self.index

    def get(self, name):
        return self.index[name]

    def register(self, name, details):
        if self.contains(name):
            raise RuntimeError("'%s' is already defined" % name)

        cached_path = os.path.join(self.registry, "%s.yay" % name)
        cached = yay.dump(yay.load_uri(details))
        open(cached_path, "w").write(cached)

        self.index[name] = {
            "name": name,
            "sidekick-file": details,
            "cached-sidekick-file": cached_path,
            }

        self.save()

