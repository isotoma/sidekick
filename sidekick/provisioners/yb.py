import StringIO
from yay.config import Config, dump
from yaybu.core.remote import RemoteRunner
from sidekick.provisioners.base import Provisioner

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
        conf = Config()

        for recipe in self.machine.project.config.get("recipes", []):
            config.load_uri(recipe)

        for recipe in self.machine.config.get("recipes", []):
            config.load_uri(recipe)

        yb = self.machine.project.config.get("yaybu", None)
        if yb:
            s = StringIO.StringIO(dump(yb))
            conf.load(s)

        yb = self.machine.config.get("yaybu", {})
        if yb:
            s = StringIO.StringIO(dump(yb))
            conf.load(s)

        with open("foo.yay", "w") as f:
            f.write(dump(conf.get()))

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

