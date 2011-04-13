
from sidekick.commands.base import ProjectCommand

class Up(ProjectCommand):

    """ Activate all environments for this project """

    name = "up"

    def do(self):
        for vm in self.project.all_vms():
            vm.power_on()
            vm.provision()


