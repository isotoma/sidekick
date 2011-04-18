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

class YaybuProvisioner(Provisioner):

    name = "yaybu"

    @staticmethod
    def can_provision(machine):
        terms = ("yaybu", "recipes", "resources")

        print machine.config, machine.project.config

        for term in terms:
            if term in machine.config or term in machine.project.config:
                return True

    def provision(self):
        conf = Config()

        for recipe in self.machine.project.config.get("recipes", []):
            config.load_uri(recipe)

        for recipe in self.machine.config.get("recipes", []):
            config.load_uri(recipe)

        yb = self.machine.project.config.get("yaybu", None)
        if yb:
            s = StringIO.StringIO(dump(yb))
            conf.load(s)

        yb = self.machine.config.get("yaybu", {})
        if yb:
            s = StringIO.StringIO(dump(yb))
            conf.load(s)

        with open("foo.yay", "w") as f:
            f.write(dump(conf.get()))

        class opts:
            log_level = "info"
            logfile = "-"
            host = "%s@%s:%s" % self.machine.vm.get_ssh_details()
            user = "root"
            ypath = []
            simulate = False
            verbose = False

        r = RemoteRunner()
        r.run(opts, ["foo.yay"])

