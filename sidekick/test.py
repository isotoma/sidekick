
from sidekick.vm import vmware

workstation = True

if workstation:
    conntype = vmware.VIX_SERVICEPROVIDER_VMWARE_WORKSTATION
    hostname = ""
    hostport = 0
    username = ""
    password = ""
    vmpoweroptions = vmware.VIX_VMPOWEROP_LAUNCH_GUI

    vmxpathinfo = "PATH_TO_VMX"
else:
    conntype = vmware.VIX_SERVICEPROVIDER_VMWARE_VI_SERVER
    hostname = "https://192.169.201.1:8333/sdk"
    hostport = 0
    username = "root"
    password = "hideme"
    vmpoweroptions = vmware.VIX_VMPOWEROP_NORMAL

    vmpathinfo = "[datastore] PATH/TO.VMX"


job = vmware.VixHost_Connect(vmware.VIX_API_VERSION,
    conntype, hostname, hostport, username, password, options, vmware.VIX_INVALID_HANDLE, None, None)

host = vmware.VixHandle()
err = VixJob_Wait(job, vmware.VIX_PROPERTY_JOB_RESULT_HANDLE, host, VIX_PROPERTY_NONE)
if err != vmware.VIX_OK:
    raise ValueError(err)

vmware.Vix_ReleaseHandle(job)


job = VixVM_Open(host, vmpathinfo, None, None)
vm = vmware.VixHandle()
err = vmware.VixJob_Wait(job, VIX_PROPERTY_JOB_RESULT_HANDLE, vm, VIX_PROPERTY_NONE)
if err != vmware.VIX_OK:
    raise ValueError(err)

vmware.Vix_ReleaseHandle(job)


job = vmware.VixVM_PowerOn(vm, vmpoweroptions, vmware.VIX_INVALID_HANDLE, None, None)
err = vmware,VixJob_Wait(job, VIX_PROPERTY_NONE)
if err != vmware.VIX_OK:
    raise ValueError(err)

vmware.Vix_ReleaseHandle(jobHandle);


job = vmware.VixVM_PowerOff(vm, vmware.VIX_VMPOWEROP_NORMAL, None, None)
err = vmware.VixJob_Wait(job, VIX_PROPERTY_NONE)
if err != vmware.VIX_OK:
    raise ValueError(err)

vmware.Vix_ReleaseHandle(job)
vmware.Vix_ReleaseHandle(vm)

vmware.VixHost_Disconnect(host)


