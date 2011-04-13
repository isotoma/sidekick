
from sidekick.provisioners.base import Provisioner

class ShellProvisioner(Provisioner):

    name = "shell"

    @staticmethod
    def can_provision(machine):
        if "script" in machine.config:
            return True

    def provision(self):
        self.machine.run_script(self.machine.config("script"))

