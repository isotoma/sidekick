
class ProviderType(type):

    providers = {}

    def __new__(meta, class_name, bases, attrs):
        cls = type.__new__(meta, class_name, bases, attrs)

        if "name" in attrs:
            if attrs["name"] in meta.providers:
                raise RuntimeError("Provider '%s' already defined" % attrs['name'])

            meta.providers[attrs["name"]] = cls

        return cls

    def find(self, project, config):
        matches = []
        for provider in self.providers.itervalues():
            if provider.probe():
                return provider


class BaseProvider(object):

    __metaclass__ = ProviderType


