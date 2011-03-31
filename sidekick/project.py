
import yay

from sidekick.machine import Machine

class Project(object):

    def __init__(self):
        self.config = yay.load_uri("Sidekick")

    def all_vms(self):
        for vm in self.config.get("vms", []):
            yield Machine(vm)

