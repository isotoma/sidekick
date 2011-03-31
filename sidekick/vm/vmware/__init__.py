
from sidekick.vm.vmware import low

class Job(object):
    """ I am a proxy for an uncompleted vmware function call """

    def __init__(self, handle):
        self.handle = handle

    def wait(self, *properties):
        err = low.vix.VixJob_Wait(self.handle, *properties)
        if err != low.VIX_OK:
            raise ValueError(err)
        low.vix.Vix_ReleaeHandle(self.handle)


class Provider(object):

    conntype = None
    hostname = ""
    hostport = 0
    username = ""
    password = ""

    def __init__(self):
        self.handle = None

    def connect(self):
        if conntype is None:
            raise NotImplementedError(self.conntype)
        j = Job(low.vix.VixHost_Connect(low.VIX_API_VERSION,
            self.conntype, self.hostname, self.hostport, self.username, self.password, 0,
            low.VIX_INVALID_HANDLE, None, None)

        self.handle = low.VixHandle()
        j.wait(low.VIX_PROPERTY_JOB_RESULT_HANDLE, byref(self.handle), low.VIX_PROPERTY_NONE)

    def disconnect(self):
        if self.handle:
            low.vix.VixHost_Disconnect(self.handle)
            self.handle = None

    def open(self, vmx):
        vm = VirtualMachine(self.handle, vmx)
        vm.open()
        return vm


class WorkstationProvider(Provider):
    conntype = low.VIX_SERVICEPROVIDER_VMWARE_WORKSTATION


class PlayerProvider(Provider):
    conntype = low.VIX_SERVICEPROVIDER_VMWARE_PLAYER


class ViServerProvider(Provider):
    def __init__(self, hostname, username, password, hostport=0):
        self.hostname = hostname
        self.hostport = hostport
        self.username = username
        self.password = password
        super(ViServerProvier, self).__init__()


class VirtualMachine(object):

    def __init__(self, host, path):
        self.host = host
        self.path = path
        self.vm = None

    def open(self):
        job = Job(low.vix.VixVM_open(self.host, self.path, None, None))
        self.vm = vmware.VixHandle()
        job.wait(low.VIX_PROPERTY_JOB_RESULT_HANDLE, byref(self.vm), low.VIX_PROPERTY_NONE)

    def power_on(self):
        job = Job(low.vix.VixVM_PowerOn(self.vm, options, low.VIX_INVALID_HANDLE, None, None))
        job.wait(vmware.VIX_PROPERTY_NONE)

    def power_off(self):
        job = Job(low.vix.VixVM_PowerOff(self.vm, vmware.VIX_VMPOWEROP_NORMAL, None, None))
        job.wait(vmware.VIX_PROPERTY_NONE)

    def release(self):
        low.vix.Vix_ReleaseHandle(self.vm)
        self.vm = None

