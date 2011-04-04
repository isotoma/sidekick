
from sidekick.command import ProjectCommand

class Down(ProjectCommand):

    """ Shutdown any active environment for this project """

    name = "down"

    def do(self):
        for vm in self.project.all_vms():
            vm.power_off()

