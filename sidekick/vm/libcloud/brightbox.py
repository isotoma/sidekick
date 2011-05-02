
from time import sleep

from libcloud.types import Provider
from libcloud.providers import get_driver

from sidekick.vm.base import BaseProvider, BaseMachine


class CloudProvider(BaseProvider):

    def __init__(self, config):
        self.config = config

        bb = get_driver(Provider.BRIGHTBOX)
        self.driver = bb(config['username'], config['key'])

    def provide(self, config):
        return CloudMachine(self.driver, config)


class CloudMachine(BaseMachine):

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def ex_wait_for_boot(self):
        while True:
            nodes = self.driver.list_nodes()
            node = filter(lambda x: x.id == self.config['id'], nodes)[0]

            if node.state == 0:
                break

            sleep(1)

    def power_on(self):
        pass
