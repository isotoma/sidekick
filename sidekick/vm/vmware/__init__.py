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


import os, shutil
from ctypes import byref, string_at, c_char_p #, create_string_buffer

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

    def get_ip(self):
        if not self.vm:
            self.connect()

        ip = c_char_p()
        job = Job(low.vix.VixVM_ReadVariable(self.vm, low.VIX_VM_GUEST_VARIABLE, "ip", 0, None, None))
        job.wait(low.VIX_PROPERTY_JOB_RESULT_VM_VARIABLE_STRING, byref(ip), low.VIX_PROPERTY_NONE)

        return string_at(ip)

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

    def put(self, path, data, chmod=None):
        self.ensure_logged_in()

        job = Job(low.vix.VixVM_CopyFileFromHostToGuest(self.vm, src_path, path, 0, low.VIX_INVALID_HANDLE, None, None))
        job.wait(low.VIX_PROPERTY_NONE)

    def run(self, *args):
        self.ensure_logged_in()

        exit_code = c_int()
        job = Job(low.vix.VixVM_RunProgramInGuest(self.vm, args[0], " ".join(args[1:], 0, low.VIX_INVALID_HANDLE, None, None)))
        job.wait(low.VIX_PROPERTY_JOB_RESULT_GUEST_PROGRAM_EXIT_CODE, byref(exit_code), low.VIX_PROPERTY_NONE)

        return exit_code.value

    def run_script(self, script, interpreter="/bin/sh"):
        self.ensure_logged_in()

        exit_code = c_int()
        job = Job(low.vix.VixVM_RunScriptIntGuest(self.vm, interpreter, script, 0, low.VIX_INVALID_HANDLE, None, None))
        job.wait(low.VIX_PROPERTY_JOB_RESULT_GUEST_PROGRAM_EXIT_CODE, byref(exit_code), low.VIX_PROPERTY_NONE)

        return exit_code.value

    def delete(self, path):
        self.ensured_logged_in()

        job = Job(low.vix.VixVM_DeleteFileInGuest(self.vm, path, None, None))
        job.wait(low.VIX_PROPERTY_NONE)

    def power_on(self):
        job = Job(low.vix.VixVM_PowerOn(self.vm, self.default_powerop_start, low.VIX_INVALID_HANDLE, None, None))
        job.wait(low.VIX_PROPERTY_NONE)

    def power_off(self):
        job = Job(low.vix.VixVM_PowerOff(self.vm, low.VIX_VMPOWEROP_NORMAL, None, None))
        job.wait(low.VIX_PROPERTY_NONE)

    def _native_clone(self, path):
        snapshot = low.VixHandle()
        #err = low.vix.VixVM_GetCurrentSnapshot(self.vm, byref(snapshot))
        #if err != low.VIX_OK:
        #    raise errors.ErrorType.get(err)

        snapshot = low.VIX_INVALID_HANDLE
        job = Job(low.vix.VixVM_Clone(self.vm, snapshot, low.VIX_CLONETYPE_LINKED, path, 0, low.VIX_INVALID_HANDLE, None, None))
        job.wait(low.VIX_PROPERTY_NONE)

        low.vix.Vix_ReleaseHandle(snapshot)

    def _manual_clone(self, path):
        src_path = os.path.dirname(self.path)
        target_path = os.path.dirname(path)
        target_container = os.path.dirname(target_path)

        if not os.path.exists(target_container):
             os.makedirs(target_container)

        shutil.copytree(src_path, target_path)

        # Mutate VMX file...
        os.rename(os.path.join(target_path, os.path.basename(self.path)),
            os.path.join(target_path, os.path.basename(path)))

    def clone(self, path):
        try:
            self._native_clone(path)
        except errors.NOT_SUPPORTED:
            self._manual_clone(path)

    def release(self):
        low.vix.Vix_ReleaseHandle(self.vm)
        self.vm = None

