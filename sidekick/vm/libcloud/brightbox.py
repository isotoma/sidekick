
from time import sleep

from libcloud.types import Provider
from libcloud.providers import get_driver

from sidekick.vm.base import BaseProvider, BaseMachine

POWERSTATES = {
    0: "running",
    }


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
        self.node = None

    def _refresh_node(self):
        nodes = filter(lambda x: x.id == self.config['id'], self.driver.list_nodes())
        self.node = nodes[0] if nodes else None

    def _wait_for_boot(self):
        while self.get_powerstate() != "running":
            sleep(1)

    def _assign_ip(self):
        if self.node.public_ip:
            return self.node.public_ip[0]

        unmapped = [ip for ip in self.driver.ex_list_cloud_ips() if not ip['server']]
        if unmapped:
            ip = unmapped[0]
        else:
            ip = self.driver.ex_create_cloud_ip()

        self.driver.ex_map_cloud_ip(ip['id'], self.node.extra['interfaces'][0]['id'])

        return ip['public_ip']

    def get_powerstate(self):
        self._refresh_node()
        return POWERSTATES[self.node.state]

    def power_on(self):
        self._refresh_node()
        if self.node:
            return

        print "Finding size (nano)"
        size = filter(lambda x: x.id == 'typ-4nssg', bb.list_sizes())[0]

        print "Finding image (lucid 10.04 i686)"
        image = filter(lambda x: x.id == 'img-hm6oj', bb.list_images())[0]

        self.node = self.driver.create_node(name=self.config['name'], size=size, image=image)

        self._wait_for_boot()
        self._assign_ip()

    def power_off(self):
        self._refresh_node()

        if not self.node:
            return

        self.driver.destroy_node(self.node)

