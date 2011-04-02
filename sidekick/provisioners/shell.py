
from sidekick.provisioner import Provisioner

class ShellProvisioner(Provisioner):

    def provision(self):
        self.machine.put(self.path. chmod=755, self.script)
        self.machine.run(self.path)
        self.machine.delete(self.path)

