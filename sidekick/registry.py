import os

class Registry(object):

    def __init__(self):
        self.environments = {}

        self.dotdir = os.path.expanduser("~/.sidekick")
        self.registry = os.path.join(self.dotdir, "registry")

    def load_environments(self):
        pass

    def save_environments(self):
        pass

    def get_environment(self, path):
        pass

    def get_all_environments(self):
        pass

