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

import shutil, random, StringIO
import paramiko

from sidekick.errors import *


class Console(object):

    def __init__(self, vm):
        self.vm = vm
        self.client = None
        self.transport = None
        self.sftp = None

    def __enter__(self):
        username, host, port = self.vm.get_ssh_details()

        self.client = paramiko.SSHClient()
        #self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port=int(port), username=username)

        self.transport = self.client.get_transport()
        self.sftp = self.client.open_sftp()

        return self

    def __exit__(self, type, value, tb):
        self.close()

    def upload(self, fp, path, mode=None):
        dst = self.sftp.open(path, 'wb')
        shutil.copyfileobj(fp, dst)
        dst.close()
        if mode:
            self.sftp.chmod(path, mode)

    def download(self, remote, local):
        self.sftp.get(remote, local)

    def remove(self, path):
        self.sftp.remove(path)

    def run(self, *args):
        chan = self.client.get_transport().open_session()
        chan.exec_command(' '.join(args))
        return chan.recv_exit_status()

    def run_script(self, script, delete=True):
        scriptpath = "/tmp/script_%04d.sh" % random.randrange(0, 9999)
        self.upload(StringIO.StringIO(script), scriptpath, 0755)
        rv = self.run(*[scriptpath])
        if delete:
            self.remove(scriptpath)
        return rv

    def close(self):
        if self.transport.is_active():
            self.sftp.close()
            self.transport.close()

