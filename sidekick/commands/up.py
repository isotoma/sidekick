
from sidekick.command import ProjectCommand

class Up(ProjectCommand):
    name = "up"

    def do(self):
        for vm in self.project.all_vms():
            vm.power_on()
            vm.provision()

