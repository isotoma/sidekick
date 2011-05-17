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


import StringIO
from yay.config import Config, dump
from yaybu.core.remote import RemoteRunner
from sidekick.provisioners.base import Provisioner
from sidekick.util import register_builtin_keys

class YaybuProvisioner(Provisioner):

    name = "yaybu"

    @staticmethod
    def can_provision(machine):
        if "yaybu" in machine.config:
            return True
        return False

    def provision(self):
        register_builtin_keys()

        conf = Config()

        recipe = self.machine.config["yaybu"]["recipe"]
        conf.load_uri(recipe)

        sk = dict(sidekick={
            "primaryip": self.machine.get_ip(),
            })
        conf.load(StringIO.StringIO(dump(sk)))

        config = conf.get()
        with open("foo.yay", "w") as f:
            f.write(dump(config))

        class opts:
            log_level = "info"
            logfile = "-"
            host = "%s@%s:%s" % self.machine.get_ssh_details()
            user = "root"
            ypath = self.machine.config["yaybu"].get("path", [])
            simulate = False
            verbose = False

        r = RemoteRunner()
        r.run(opts, ["foo.yay"])

