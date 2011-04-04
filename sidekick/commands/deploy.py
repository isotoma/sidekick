
from sidekick.command import ProjectCommand

class Deploy(ProjectCommand):

    name = "deploy"

    def do(self):
        for vm in self.project.all_vms():
            vm.provision()

