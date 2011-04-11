

class Provider(object):

    style = None

    def __init__(self):
        self.globl = None

    def connect(self):
        cwd = os.getcwd()
        vbp = os.environ.get("VBOX_PROGRAM_PATH")
        if not vbp:
            if os.path.isfile(cwd, "VirtualBox"):
                vbp = cwd
            if os.path.isfile(cwd, "VirtualBox.exe"):
                vbp = cwd
            os.environ["VBOX_PROGRAM_PATH"] = vbp
            sys.path.append(os.path.join(vbp, "sdk", "installer"))

        self.globl = VirtualBoxManager(self.style, None)
        self.mgr = self.globl.mgr
        self.vb = self.globl.vb
        self.ifaces = self.globl.constants
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

    def open(self, path):
        vm = None
        return vm


class WebProvider(object):
    style = None


class VirtualMachine(object):

    def __init__(self, host, path, default_powerop_start=low.VIX_VMPOWEROP_NORMAL):
        pass

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
        pass

    def power_off(self):
        pass

    def clone(self, path):
        pass

    def release(self):
        pass

