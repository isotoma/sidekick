
import logging
from time import sleep

from libcloud.compute.types import Provider, NodeState
from libcloud.compute.providers import get_driver

from sidekick.vm.base import BaseProvider, BaseMachine
from sidekick.errors import SidekickError


POWERSTATES = {
    NodeState.RUNNING: "running",
    NodeState.REBOOTING: "waiting",
    NodeState.TERMINATED: "terminated",
    NodeState.PENDING: "waiting",
    NodeState.UNKNOWN: "unknown",
    }


class CloudProvider(BaseProvider):

    name = "brightbox"

    def __init__(self, config):
        self.config = config

        bb = get_driver(Provider.BRIGHTBOX)
        self.driver = bb(config['username'], config['key'])

    def provide(self, config):
        return CloudMachine(self.driver, config)


class CloudMachine(BaseMachine):

    def __init__(self, driver, config):
        self.logger = logging.getLogger("sidekick.vm.libcloud.brightbox.CloudMachine")
        self.driver = driver
        self.config = config
        self.node = None

    def _refresh_node(self):
        nodes = filter(lambda x: x.name == self.config['name'], self.driver.list_nodes())
        self.node = nodes[0] if nodes else None

    def _wait_for_boot(self):
        self.logger.debug("Waiting for boot")
        while self.get_powerstate() != "running":
            self.logger.debug("Still waiting")
            sleep(1)
        self.logger.debug("Booted")

    def _assign_ip(self):
        self.logger.debug("Asked to assign ip")
        if self.node.public_ip:
            self.logger.debug("Already assigned ip: %s", self.node.public_ip[0])
            return self.node.public_ip[0]

        unmapped = [ip for ip in self.driver.ex_list_cloud_ips() if not ip['server']]
        if unmapped:
            ip = unmapped[0]
            self.logger.debug("Reusing %s", ip['public_ip'])
        else:
            ip = self.driver.ex_create_cloud_ip()
            self.logger.debug("Claimed new ip %s", ip['public_ip'])

        self.driver.ex_map_cloud_ip(ip['id'], self.node.extra['interfaces'][0]['id'])

        return ip['public_ip']

    def get_powerstate(self):
        self._refresh_node()
        if not self.node:
            return "undefined"
        return POWERSTATES[self.node.state]

    def get_ip(self):
        self._refresh_node()
        return self.node.public_ip[0]

    def get_size(self):
        self.logger.debug("Finding size")
        size = filter(lambda x: x.id == 'typ-4nssg', self.driver.list_sizes())[0]
        self.logger.info("Found size: %s", size.name)
        return size

    def get_image(self):
        self.logger.debug("Finding image")
        image = filter(lambda x: x.id == 'img-4gqhs', self.driver.list_images())[0]
        self.logger.info("Found image: %s", image.name)
        return image

    def power_on(self):
        self.logger.debug("Asked to power on")
        powerstate = self.get_powerstate()

        if powerstate == "terminated":
            raise SidekickError("A VM with the name '%s' already exists in a terminated state, cannot perform any operations on it" % self.config['name'])

        if powerstate != "undefined":
            self.logger.debug("Already powered on")
            return

        self.node = self.driver.create_node(
            name=self.config['name'],
            size=self.get_size(),
            image=self.get_image())

        self._wait_for_boot()
        self._assign_ip()

    def destroy(self):
        self.logger.debug("Asked to destroy")
        powerstate = self.get_powerstate()

        if not self.node or powerstate == "terminated":
            self.logger.debug("Already destroyed")
            return

        self.driver.destroy_node(self.node)

