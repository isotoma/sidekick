
from sidekick.command import ProjectCommand

class Down(ProjectCommand):
    name = "down"

    def do(self):
        for vm in self.all_vms():
            vm.stop()

