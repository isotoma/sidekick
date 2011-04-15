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

from sidekick.progress import Progress as BaseProgress
from sidekick.vm import BaseProvider

class Provider(BaseProvider):

    name = "virtualbox"
    style = None

    def __init__(self):
        self.globl = None

    @classmethod
    def probe(cls):
        return True

    def provide(self):
        if not self.globl:
            self.connect()

        lookfor = 'wonderflonium' #sigh

        machines = self.globl.getArray(self.vb, 'machines')
        for machine in machines:
            if machine.name == lookfor or machine.id == lookfor:
                return VirtualMachine(self, machine)

    def connect(self):
        cwd = os.getcwd()
        vbp = os.environ.get("VBOX_PROGRAM_PATH")
        if not vbp:
            if os.path.isfile(os.path.join(cwd, "VirtualBox")):
                vbp = cwd
            if os.path.isfile(os.path.join(cwd, "VirtualBox.exe")):
                vbp = cwd
            if vbp:
                os.environ["VBOX_PROGRAM_PATH"] = vbp
                sys.path.append(os.path.join(vbp, "sdk", "installer"))

        from vboxapi import VirtualBoxManager

        self.globl = VirtualBoxManager(self.style, None)
        self.mgr = self.globl.mgr
        self.vb = self.globl.vbox
        self.const = self.globl.constants
        self.remote = self.globl.remote
        self.type = self.globl.type

    def disconnect(self):
        self.mgr = None
        self.vb = None
        self.ifaces = None
        self.remote = None
        self.type = None

        if self.globl:
            self.globl.deinit()
            self.globl = None


class WebProvider(object):
    style = None


class Progress(BaseProgress):

    def __init__(self, globl, progress_object):
        BaseProgress.__init__(self, 100)
        self.globl = globl
        self.progress_object = progress_object

    def do(self):
        p = self.progress_object
        try:
            while not p.completed:
                self.progress(p.percent)
                p.waitForCompletion(100)
                self.globl.waitForEvents(0)
            self.finish()
            return 1
        except KeyboardInterrupt:
            if p.cancelable:
                print "Canceling..."
                p.cancel()
                self.finish()
            raise


class Session(object):

    def __init__(self, globl, machine):
        self.globl = globl
        self.mgr = self.globl.mgr
        self.vb = self.globl.vbox
        self.const = self.globl.constants
        self.remote = self.globl.remote
        self.type = self.globl.type

        self.machine = machine

    def __enter__(self):
        self.session = self.mgr.getSessionObject(self.vb)
        #self.vb.openExistingSession(self.session, self.machine.id)
        self.machine.lockMachine(self.session, self.const.LockType_Shared)

        if self.session.state != self.const.SessionState_Locked:
            #self.session.close()
            self.session = None
            raise RuntimeError("Session to '%s' in wrong state: %s" % (self.macine.name, self.session.state))

        return self.session

    def __exit__(self, *args):
        if self.session:
            #self.session.close()
            self.session = None


class VirtualMachine(object):

    username = "sidekick"
    password = "sidekick"

    def __init__(self, provider, machine):
        self.provider = provider

        self.globl = provider.globl
        self.mgr = self.globl.mgr
        self.vb = self.globl.vbox
        self.const = self.globl.constants
        self.remote = self.globl.remote
        self.type = self.globl.type

        self.machine = machine

    def get_ip(self):
        return ""

    def get_powerstate(self):
        #self.machine.state == self.const.MachineState_Aborted
        #self.machine.state == self.const.MachineState_Saved
        #self.machine.state == self.const.MachineState_Saving
        #self.machine.state == self.const.MachineState_Paused

        if self.machine.state == self.const.MachineState_Stopping:
            return "powering-off"
        if self.machine.state == self.const.MachineState_PoweredOff:
            return "off"
        if self.machine.state == self.const.MachineState_Starting:
            return "powering-on"
        if self.machine.state == "Running":
            return "running"

    def open(self):
        pass

    def put(self, path, data, chmod=None):
        with Session(self.globl, self.machine) as s:
            progress = s.console.guest.copyToGuest(SRC, path, USERNAME, PASSWORD, 0)
            Progress(self.globl, progress).do()

    def run(self, *args):
        with Session(self.globl, self.machine) as s:
            progress = s.console.guest.executeProgress(args[0], 0, args[1:], [], self.username, self.password, 0)
            Progress(self.globl, progress).do()

        return 1 # exit code

    def run_script(self, script, interpreter="/bin/sh"):
        return 1 #exit_code

    def delete(self, path):
        self.run("rm", path)

    def power_on(self):
        session = self.mgr.getSessionObject(self.vb)

        if hasattr(self.machine, "launchVMProcess"):
            progress = self.machine.launchVMProcess(session, "gui", '')
        else:
            progress = self.vb.openRemoteSession(session, self.machine.id, "gui", '')

        Progress(self.globl, progress).do()

        if hasattr(self.machine, "unlockMachine"):
            session.unlockMachine()

    def power_off(self):
        with Session(self.globl, self.machine) as s:
            s.console.powerDown()

    def clone(self, path):
        pass

    def release(self):
        pass


if __name__ == "__main__":
    v = Provider().provide()
    v.power_on()
    v.power_off()

