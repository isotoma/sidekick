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

import paramiko, time, shutil, random
import StringIO

from sidekick.provisioners import ProvisionerType
from sidekick.console import Console
from sidekick.errors import SidekickError


class ProviderType(type):

    providers = {}

    def __new__(meta, class_name, bases, attrs):
        cls = type.__new__(meta, class_name, bases, attrs)

        if "name" in attrs:
            if attrs["name"] in meta.providers:
                raise SidekickError("Provider '%s' already defined" % attrs['name'])

            meta.providers[attrs["name"]] = cls

        return cls

    @classmethod
    def get_defaults(cls):
        defaults = {}
        for p in cls.providers.values():
            defaults.update(p.get_defaults())
        return defaults


class BaseProvider(object):

    __metaclass__ = ProviderType

    @classmethod
    def get_defaults(self):
        return {}


class BaseMachine(object):

    def __init__(self, config):
        self.config = config

    def provision(self, backend=None, **kwargs):
        #if not self.is_running():
        #    raise errors.VmNotRunning()

        print "Provisioning vm..."

        p = None
        if backend:
            try:
                p = ProvisionerType.provisioners[backend]
            except KeyError:
                raise SidekickError("There is no such provisioner: '%s'" % backend)
        else:
            for p in ProvisionerType.provisioners.values():
                if p.can_provision(self):
                    break
            else:
                raise SidekickError("Cannot find a suitable provisioner")

        # Actually do this thing
        p(self).provision(**kwargs)


class BaseMachineWithSSHConsole(BaseMachine):

    def __init__(self, config):
        super(BaseMachineWithSSHConsole, self).__init__(config)

        self._client = None
        self._transport = None
        self._sftp = None

    @property
    def client(self):
        if not self._client:
            username, host, port = self.get_ssh_details()

            self._client = paramiko.SSHClient()
            #self._client.load_system_host_keys()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(host, port=int(port), username=username)
        return self._client

    @property
    def transport(self):
        if not self._transport:
            self.transport = self.client.get_transport()
        return self._transport

    @property
    def sftp(self):
        if not self._sftp:
            self._sftp = self.client.open_sftp()
        return self._sftp

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

    def call(self, *args):
        chan = self.client.get_transport().open_session()
        chan.exec_command(' '.join(args))

        stdout = ""
        stderr = ""

        while not chan.exit_status_ready():
            if chan.recv_ready():
                stdout += chan.recv(9999)
            if chan.recv_stderr_ready():
                stderr += chan.recv_stderr(9999)
            time.sleep(0.1)

        return stdout, stderr, chan.recv_exit_status()

    def script(self, script, delete=True):
        scriptpath = "/tmp/script_%04d.sh" % random.randrange(0, 9999)
        self.upload(StringIO.StringIO(script), scriptpath, 0755)
        rv = self.call(*[scriptpath])
        if delete:
            self.remove(scriptpath)
        return rv

    def close(self):
        if self.transport.is_active():
            self.sftp.close()
            self.transport.close()

