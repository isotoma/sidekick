
from yaybu.core.remote import RemoteRunner

from sidekick.provisioner import Provisioner

class YaybuProvisioner(Provisioner):

    name = "yaybu"

    @staticmethod
    def can_provision(machine):
        terms = ("yaybu", "recipes", "resources")

        print machine.config, machine.project.config

        for term in terms:
            if term in machine.config or term in machine.project.config:
                return True

    def provision(self):
        class opts:
            log_level = "info"
            logfile = "-"
            host = self.machine.get_ip()
            user = "root"
            ypath = []
            simulate = False
            verbose = False

        r = RemoteRunner()
        r.run(opts, ["foo.yay"])

