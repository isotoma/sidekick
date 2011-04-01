from ctypes import byref
from sidekick.vm.vmware import low, errors

class Job(object):
    """ I am a proxy for an uncompleted vmware function call """

    def __init__(self, handle):
        self.handle = handle

    def wait(self, *properties):
        err = low.vix.VixJob_Wait(self.handle, *properties)
        if err != low.VIX_OK:
            raise errors.ErrorType.get(err)
        low.vix.Vix_ReleaseHandle(self.handle)


class Provider(object):

    conntype = None
    hostname = ""
    hostport = 0
    username = ""
    password = ""
    default_powerop_start = low.VIX_VMPOWEROP_LAUNCH_GUI

    def __init__(self):
        self.handle = None

    def connect(self):
        if self.conntype is None:
            raise NotImplementedError(self.conntype)
        j = Job(low.vix.VixHost_Connect(low.VIX_API_VERSION,
            self.conntype, self.hostname, self.hostport, self.username, self.password, 0,
            low.VIX_INVALID_HANDLE, None, None))

        self.handle = low.VixHandle()
        j.wait(low.VIX_PROPERTY_JOB_RESULT_HANDLE, byref(self.handle), low.VIX_PROPERTY_NONE)

    def disconnect(self):
        if self.handle:
            low.vix.VixHost_Disconnect(self.handle)
            self.handle = None

    def open(self, vmx):
        vm = VirtualMachine(self.handle, vmx, default_powerop_start=self.default_powerop_start)
        vm.open()
        return vm


class WorkstationProvider(Provider):
    conntype = low.VIX_SERVICEPROVIDER_VMWARE_WORKSTATION


class PlayerProvider(Provider):
    conntype = low.VIX_SERVICEPROVIDER_VMWARE_PLAYER


class ViServerProvider(Provider):
    default_powerop_start = low.VIX_VMPOWEROP_NORMAL

    def __init__(self, hostname, username, password, hostport=0):
        self.hostname = hostname
        self.hostport = hostport
        self.username = username
        self.password = password
        super(ViServerProvier, self).__init__()


class VirtualMachine(object):

    def __init__(self, host, path, default_powerop_start=low.VIX_VMPOWEROP_NORMAL):
        self.host = host
        self.path = path
        self.vm = None
        self.default_powerop_start = default_powerop_start

    def get_powerstate(self):
        if not self.vm:
            self.connect()

        powerstate = low.VixPowerState()
        err = low.vix.Vix_GetProperties(self.vm, low.VIX_PROPERTY_VM_POWER_STATE, byref(powerstate), low.VIX_PROPERTY_NONE)
        if err != low.VIX_OK:
            raise errors.ErrorType.get(err)

        powerstate = powerstate.value

        if powerstate & low.VIX_POWERSTATE_POWERED_ON:
            if powerstate & low.VIX_POWERSTATE_TOOLS_RUNNING:
                return "running"
            return "nearly-running"
        elif powerstate & low.VIX_POWERSTATE_POWERING_ON:
            return "powering-on"
        elif powerstate & low.VIX_POWERSTATE_POWERING_OFF:
            return "powering-off"
        elif powerstate & low.VIX_POWERSTATE_POWERED_OFF:
            return "off"
        elif powerstate & low.VIX_POWERSTATE_SUSPENDING:
            return "powering-off"
        elif powerstate & low.VIX_POWERSTATE_SUSPENDED:
            return "off"
        elif powerstate & low.VIX_POWERSTATE_RESETTING:
            return "powering-on"
        else:
            return "meh-fixme, %d" % powerstate

    def open(self):
        job = Job(low.vix.VixVM_Open(self.host, self.path, None, None))
        self.vm = low.VixHandle()
        job.wait(low.VIX_PROPERTY_JOB_RESULT_HANDLE, byref(self.vm), low.VIX_PROPERTY_NONE)

    def power_on(self):
        job = Job(low.vix.VixVM_PowerOn(self.vm, self.default_powerop_start, low.VIX_INVALID_HANDLE, None, None))
        job.wait(low.VIX_PROPERTY_NONE)

    def power_off(self):
        job = Job(low.vix.VixVM_PowerOff(self.vm, low.VIX_VMPOWEROP_NORMAL, None, None))
        job.wait(low.VIX_PROPERTY_NONE)

    def release(self):
        low.vix.Vix_ReleaseHandle(self.vm)
        self.vm = None

