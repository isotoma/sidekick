
import os

import yay

from sidekick.errors import NoProjectFile
from sidekick.machine import Machine

class Project(object):

    def __init__(self):
        if not os.path.exists("Sidekick"):
            raise NoProjectFile("No project information exists, run sidekick init?")

        self.config = yay.load_uri("Sidekick")

    def all_vms(self):
        for vm in self.config.get("environments", []):
            yield Machine(self, vm)

