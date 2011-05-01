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

class Nc(ProjectCommand):

    """
    nc into an environent

    This allows you to run nc for a Sidekick managed VM without knowing its
    IP. For example, you could use this with an ssh ProxyCommand directive
    to allow any SSH using tools (nautilus, libvirt, scp) to transparently
    connect to $project.sidekick
    """

    name = "nc"

    def setup_optparse(self, parser, args):
        args.append("hostname")
        args.append("port")

    def do(self):
        #FIXME: Need to pick a specific node...
        nodes = self.get_nodes()
        node = list(nodes)[0]

        #if not vm.is_running():
        #    raise errors.VmNotRunning()

        command = ["nc"]
        command.append(node.get_ip())
        command.append(self.args[1])

        os.execv("/usr/bin/nc", command)


