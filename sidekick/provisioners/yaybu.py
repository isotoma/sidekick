
from yaybu.core.remote import RemoteRunner

from sidekick.provisioner import Provisioner

class YaybuProvisioner(Provisioner):

    @staticmethod
    def can_provision(machine):
        terms = ("yaybu", "recipes", "resources")

        for term in terms:
            if term in machine.config or term in machine.project.config:
                return True

    def provision(self):
        r = RemoteRunner()
        r.run(opts, [])

