
from yaybu.core.remote import RemoteRunner

from sidekick.provisioner import Provisioner

class YaybuProvisioner(Provisioner):

    def run(self, ip):
        r = RemoteRunner()
        r.run(opts, [])

