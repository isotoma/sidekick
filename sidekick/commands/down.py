
from sidekick.command import ProjectCommand

class Down(ProjectCommand):
    name = "down"

    def do(self):
        for vm in self.project.all_vms():
            vm.power_off()

