import os

from sidekick.progress import Progress as BaseProgress
from sidekick.vm import BaseProvider

class Provider(BaseProvider):

    style = None

    def __init__(self):
        self.globl = None

    @classmethod
    def probe(cls):
        return True

    def provide(self):
        if not self.globl:
            self.connect()

        lookfor = 'lucid'

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
            return 1
        except KeyboardInterrupt:
            if p.cancelable:
                print "Canceling..."
                p.cancel()
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
        return "running"

    def open(self):
        pass

    def put(self, path, data, chmod=None):
        pass

    def run(self, *args):
        return 1 # exit code

    def run_script(self, script, interpreter="/bin/sh"):
        return 1 #exit_code

    def delete(self, path):
        pass

    def power_on(self):
        session = self.mgr.getSessionObject(self.vb)
        progress = vb.openRemoteSession(session, uuid, type, "")
        Progress(self.globl, progress).do()

    def power_off(self):
        with Session(self.globl, self.machine) as s:
            s.console.powerDown()

    def clone(self, path):
        pass

    def release(self):
        pass


if __name__ == "__main__":
    v = Provider().provide()
    v.power_off()

