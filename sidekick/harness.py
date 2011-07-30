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

from yaybu.harness.fixture import Fixture


class NodeFixture(Fixture):

    def __init__(self, name, base, fixture):
        super(NodeFixture, self).__init__()
        self.name = name
        self.base = base
        self.fixture = fixture
        self.vm = None
        self.cluster = None

    def setParent(self, cluster):
        self.cluster = cluster
        setattr(cluster, self.name, self)

    def setUp(self):
        self.vm = self.cluster.env.provide({
            "name": self.name,
            "base": self.base,
            })
        self.vm.power_on()

    def __getattr__(self, param):
        return getattr(self.vm, param)


class ClusterFixture(Fixture):

    def __init__(self, nodes=None):
        super(ClusterFixture, self).__init__()
        self.nodes = nodes or []
        [n.setParent(self) for n in self.nodes]

    def setUp(self):
        for n in self.nodes:
            n.setUp()
        for n in self.nodes:
            n.vm.provision(backend="yaybu", conf=n.fixture)

    def cleanUp(self):
        for node in self.nodes:
            try:
                node.cleanUp()
            except:
                pass

            node.destroy()

