# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Cluster(object):

    def __init__(self, name, environment, config):
        self.name = name
        self.environment = environment
        self.config = config

    def _get_machine(self, config):
        return self.environment.provide(config)

    def get_node(self, name):
        for node in self.config.get("nodes", []):
            if node['name'] == name:
                break
        else:
            raise KeyError("Node '%s' is not defined" % name)

        return self._get_machine(node)

    def get_nodes(self):
        for node in self.config.get("nodes", []):
            yield self._get_machine(node)

