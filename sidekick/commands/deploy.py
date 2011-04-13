
from sidekick.commands.base import ProjectCommand

class Deploy(ProjectCommand):

    """ Deploy the latest environment configuration. """

    name = "deploy"

    def do(self):
        for vm in self.project.all_vms():
            vm.provision()

