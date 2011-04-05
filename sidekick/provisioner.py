

class ProvisionerType(type):

    provisioners = {}

    def __new__(meta, name, bases, new_attrs):
        cls = type.__new__(meta, name, bases, new_attrs)

        if "name" in new_attrs:
            meta.provisionsers[new_attrs["name"]] = cls

        return cls


class Provisioner(object):
    __metaclass__ = ProvisionerType

    def __init__(self, machine):
        self.machine = machine

    def provision(self):
        raise NotImplementedError(self.provision)

