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

