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

from sidekick.errors import SidekickError

class BaseRegistry(object):

    def __init__(self, defaults_fn=lambda: {}):
        datadir = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        self.dotdir = os.path.join(datadir, "sidekick")
        self.registry = os.path.join(self.dotdir, "registry")
        self.index_file = os.path.join(self.registry, self.file)

        if not os.path.exists(self.registry):
            os.makedirs(self.registry)

        if os.path.exists(self.index_file):
            self.index = yay.load_uri(self.index_file)
        else:
            self.index = defaults_fn()
            self.save()

    def save(self):
        open(self.index_file, "w").write(yay.dump(self.index))

    def all(self):
        return self.index.keys()

    def contains(self, name):
        return name in self.index

    def get(self, name):
        return self.index[name]

    def delete(self, name):
        del self.index[name]
        self.save()


class Instances(BaseRegistry):

    file = "instances.yay"

    def register(self, name, env, details):
        if self.contains(name):
            raise SidekickError("'%s' is already defined" % name)

        cached_path = os.path.join(self.registry, "%s.yay" % name)
        cached = yay.dump(yay.load_uri(details))
        open(cached_path, "w").write(cached)

        self.index[name] = {
            "name": name,
            "env": env,
            "sidekick-file": details,
            "cached-sidekick-file": cached_path,
            }

        self.save()

    def delete(self, name):
        if self.contains(name):
            path = self.get(name)["cached-sidekick-file"]
            if os.path.exists(path):
                os.unlink(path)

        super(Instances, self).delete(name)


class Environments(BaseRegistry):

    file = "environments.yay"

    def get_default(self):
        return self.all()[0]

    def register(self, name, type, config):
        if self.contains(name):
            raise SidekickError("'%s' is already defined")

        env = {
            "name": name,
            "type": type,
            }
        env.update(config)

        self.index[name] = env
        self.save()

