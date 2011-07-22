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
from sidekick import util
from sidekick.provisioners.base import Provisioner
from sidekick.util import register_builtin_keys


bootstrap = """
#! /bin/sh

test ! -f /usr/bin/yaybu || exit 0

# Install yaybu from nightly PPA
cat << EOF | sudo tee /etc/apt/sources.list.d/yaybu.list
deb http://ppa.launchpad.net/yaybu-team/yaybu-nightly/ubuntu lucid main
deb-src http://ppa.launchpad.net/yaybu-team/yaybu-nightly/ubuntu lucid main
EOF

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A899DA54
sudo apt-get update
sudo apt-get install -y -q python-yaybu

# Grant passwordless root to Yaybu
cat << HERE | sudo tee /etc/sudoers
# /etc/sudoers
#
# This file MUST be edited with the 'visudo' command as root.
#
# See the man page for details on how to write a sudoers file.
#

Defaults        env_reset

# Host alias specification

# User alias specification

# Cmnd alias specification
Cmnd_Alias YAYBU = /usr/bin/yaybu

# User privilege specification
root    ALL=(ALL) ALL

# Members of the admin group may gain root privileges
%admin ALL=(ALL) NOPASSWD: ALL

# Allow members of the admin group to run yaybu as root without
# providing a password
%admin ALL=(root) NOPASSWD: YAYBU

HERE
""".strip()


class YaybuProvisioner(Provisioner):

    name = "yaybu"

    @staticmethod
    def can_provision(machine):
        if "yaybu" in machine.config:
            return True
        return False

    def bootstrap(self):
        self.machine.script(bootstrap)

    def provision(self, **kwargs):
        register_builtin_keys()

        self.bootstrap()

        conf = Config()

        sk = dict(sidekick={
            "host": {
                "ips": dict(util.interfaces()),
                },
            "primaryip": self.machine.get_ip(),
            })
        conf.load(StringIO.StringIO(dump(sk)))

        if "recipe" in kwargs:
            conf.load_uri(kwargs['recipe'])

        if "conf" in kwargs:
            conf.load(StringIO.StringIO(kwargs['conf']))

        config = conf.get()
        with open("foo.yay", "w") as f:
            f.write(dump(config))

        class opts:
            log_level = "info"
            logfile = "-"
            host = "%s@%s:%s" % self.machine.get_ssh_details()
            user = "root"
            ypath = kwargs.get("path", [])
            simulate = False
            verbose = False
            resume = True
            no_resume = False
            env_passthrough = []

        r = RemoteRunner()
        #r.load_host_keys(
        r.set_missing_host_key_policy("no")

        rv = r.run(opts, ["foo.yay"])

        print rv

