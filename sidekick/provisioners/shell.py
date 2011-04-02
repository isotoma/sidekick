
from sidekick.provisioner import Provisioner

class ShellProvisioner(Provisioner):

    def provision(self):
        self.machine.run_script(self.script)

