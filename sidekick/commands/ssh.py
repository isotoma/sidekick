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
        vms = self.project.all_vms()
        vm = list(vms)[0]

        #if not vm.is_running():
        #    raise errors.VmNotRunning()

        command = ["ssh", "-A"]

        # if deploy_user:
        #     command.extend(['-l', deploy_user])

        command.append(vm.get_ip())

        os.execv("/usr/bin/ssh", command)


