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

from sidekick.errors import SidekickError
from sidekick.progress import Progress as BaseProgress
from sidekick.vm import BaseProvider, BaseMachine
from sidekick.images import ImageRegistry

class Provider(BaseProvider):

    name = "virtualbox"
    parameters = [
    ]

    style = None

    def __init__(self, config):
        self.globl = None

    def provide(self, machine):
        if not self.globl:
            self.connect()

        lookfor = machine["name"]

        machines = self.globl.getArray(self.vb, 'machines')
        for m in machines:
            if m.name == lookfor or m.id == lookfor:
                return VirtualMachine(self, machine)

        # FIXME: Would be nice to support this in future...
        #for m in machines:
        #    if m.name == machine["base"] or m.id == machine["base"]:
        #        base = VirtualMachine(self, {"name": machine["base"]})
        #        break
        #else:
        #    raise SidekickError("Unable to find base '%s'" % machine['base'])

        vmdir = os.path.join(os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share')), "sidekick", "vbox")
        vmpath = os.path.join(vmdir, machine["name"], "%s.box" % machine["name"])
        vdipath = os.path.join(vmdir,  machine["name"], "%s.vdi" % machine["name"])

        if not os.path.exists(vdipath):
            base_path = ImageRegistry().get_image(machine['base'])

            if os.path.isdir(base_path):
                vdis = glob.glob(os.path.join(base_path, "*.vdi"))

                if not vdis:
                    raise SidekickError("%s is not a valid base image" % machine['base'])

                base_path = vdis[0]

            base = self.vb.openMedium(base_path, self.const.DeviceType_HardDisk, self.const.AccessMode_ReadOnly)
            target = self.vb.createHardDisk("vdi", vdipath)
            progress = base.cloneTo(target, self.const.MediumVariant_Standard, None)
            Progress(self.globl, progress).do()
        else:
            target = self.vb.openMedium(vdipath, self.const.DeviceType_HardDisk, self.const.AccessMode_ReadOnly)

        if not os.path.exists(vmpath):
            desired_ostype = machine.get("os-type", "Ubuntu_64")

            matching_ostype = [x for x in self.globl.getArray(self.vb, "guestOSTypes") if x.id.lower() == desired_ostype.lower()]
            if len(matching_ostype) == 0:
                raise SidekickError("Unable to find OS Type '%s'" % desired_ostype)

            m = self.vb.createMachine(vmpath, machine['name'], matching_ostype[0].id, "", False)
            m.saveSettings()
        else:
            print "opening"
            m = self.vb.openMachine(vmpath)

        # FIXME: Decide whether this is right...
        self.vb.registerMachine(m)

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
        if hasattr(self.machine, "lockMachine"):
            self.machine.lockMachine(self.session, self.const.LockType_Shared)
            desired_session_state = self.const.SessionState_Locked
        else:
            self.vb.openExistingSession(self.session, self.machine.id)
            desired_session_state = self.const.SessionState_Open

        if self.session.state != desired_session_state:
            #self.session.close()
            self.session = None
            raise SidekickError("Session to '%s' in wrong state: %s" % (self.macine.name, self.session.state))

        return self.session

    def __exit__(self, *args):
        if self.session:
            #self.session.close()
            self.session = None


class VirtualMachine(BaseMachine):

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

    def get_ssh_details(self):
        for from_port, to_port in self.ex_enumerate_forwarding():
            if from_port == "22":
                port = to_port
                break
        else:
            #FIXME: Need a better port allocator
            self.ex_forward_port(22, 2222)
            port = 2222

        return "sidekick", "localhost", port

    def ex_enumerate_forwarding(self):
        adapter = self.machine.getNetworkAdapter(0)
        redirects = self.globl.getArray(adapter.natDriver, 'redirects')
        for line in redirects:
            name, proto, host_ip, host_port, guest_ip, guest_port = line.split(",")
            yield guest_port, host_port

    def ex_forward_port(self, from_port, to_port):
        adapter = self.machine.getNetworkAdapter(0)

        name = "%s-%s" % (from_port, to_port)
        adapter.natDriver.addRedirect(name, self.const.NATProtocol_TCP, "", from_port, "", to_port)

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

