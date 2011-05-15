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


import os

from sidekick import errors
from sidekick.commands.base import ProjectCommand

class Ssh(ProjectCommand):

    """ SSH into an environent """

    name = "ssh"

    def do(self):
        #FIXME: Pick a VM:
        #  - if there is more than 1 defined, must be specified
        #  - if there is only 1 defined, ssh into that
        #  - if there is only 1 defined and the name is specified it
        #    must be right
        nodes = self.get_current_cluster().get_nodes()
        node = list(nodes)[0]

        #if not vm.is_running():
        #    raise errors.VmNotRunning()

        command = ["ssh", "-A", "-o", "UserKnownHostsFile /dev/null", "-o", "StrictHostKeyChecking no"]

        #["-o", "IdentifyFile %s" % "path/to/key"]

        user, host, port = node.get_ssh_details()

        command.extend(["-l", user, "-p", str(port), host])
        os.execv("/usr/bin/ssh", command)


