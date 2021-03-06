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


from ctypes import *

# user defined types
VixHandle = c_int
VixHandleType = c_int
VixError = c_uint64
VixPropertyType = c_int
VixPropertyID = c_int
VixEventType = c_int
VixHostOptions = c_int
VixServiceProvider = c_int
VixFindItemType = c_int
VixVMOpenOptions = c_int
VixPumpEventsOptions = c_int
VixVMPowerOpOptions = c_int
VixVMDeleteOptions = c_int
VixPowerState = c_int
VixToolsState = c_int
VixRunProgramOptions = c_int
VixRemoveSnapshotOptions = c_int
VixCreateSnapshotOptions = c_int
VixMsgSharedFolderOptions = c_int
VixCloneType = c_int
VixEventProc = CFUNCTYPE(VixHandle,
    VixEventType,
    VixHandle,
    c_void_p)

# constant definitions
VIX_INVALID_HANDLE = 0
VIX_HANDLETYPE_NONE = 0
VIX_HANDLETYPE_HOST = 2
VIX_HANDLETYPE_VM = 3
VIX_HANDLETYPE_NETWORK = 5
VIX_HANDLETYPE_JOB = 6
VIX_HANDLETYPE_SNAPSHOT = 7
VIX_HANDLETYPE_PROPERTY_LIST = 9
VIX_HANDLETYPE_METADATA_CONTAINER = 11
VIX_OK = 0

VIX_PROPERTYTYPE_ANY = 0
VIX_PROPERTYTYPE_INTEGER = 1
VIX_PROPERTYTYPE_STRING = 2
VIX_PROPERTYTYPE_BOOL = 3
VIX_PROPERTYTYPE_HANDLE = 4
VIX_PROPERTYTYPE_INT64 = 5
VIX_PROPERTYTYPE_BLOB = 6
VIX_PROPERTY_NONE = 0
VIX_PROPERTY_META_DATA_CONTAINER = 2
VIX_PROPERTY_HOST_HOSTTYPE = 50
VIX_PROPERTY_HOST_API_VERSION = 51
VIX_PROPERTY_VM_NUM_VCPUS = 101
VIX_PROPERTY_VM_VMX_PATHNAME = 103
VIX_PROPERTY_VM_VMTEAM_PATHNAME = 105
VIX_PROPERTY_VM_MEMORY_SIZE = 106
VIX_PROPERTY_VM_READ_ONLY = 107
VIX_PROPERTY_VM_NAME = 108
VIX_PROPERTY_VM_GUESTOS = 109
VIX_PROPERTY_VM_IN_VMTEAM = 128
VIX_PROPERTY_VM_POWER_STATE = 129
VIX_PROPERTY_VM_TOOLS_STATE = 152
VIX_PROPERTY_VM_IS_RUNNING = 196
VIX_PROPERTY_VM_SUPPORTED_FEATURES = 197
VIX_PROPERTY_VM_IS_RECORDING = 236
VIX_PROPERTY_VM_IS_REPLAYING = 237
VIX_PROPERTY_JOB_RESULT_ERROR_CODE = 3000
VIX_PROPERTY_JOB_RESULT_VM_IN_GROUP = 3001
VIX_PROPERTY_JOB_RESULT_USER_MESSAGE = 3002
VIX_PROPERTY_JOB_RESULT_EXIT_CODE = 3004
VIX_PROPERTY_JOB_RESULT_COMMAND_OUTPUT = 3005
VIX_PROPERTY_JOB_RESULT_HANDLE = 3010
VIX_PROPERTY_JOB_RESULT_GUEST_OBJECT_EXISTS = 3011
VIX_PROPERTY_JOB_RESULT_GUEST_PROGRAM_ELAPSED_TIME = 3017
VIX_PROPERTY_JOB_RESULT_GUEST_PROGRAM_EXIT_CODE = 3018
VIX_PROPERTY_JOB_RESULT_ITEM_NAME = 3035
VIX_PROPERTY_JOB_RESULT_FOUND_ITEM_DESCRIPTION = 3036
VIX_PROPERTY_JOB_RESULT_SHARED_FOLDER_COUNT = 3046
VIX_PROPERTY_JOB_RESULT_SHARED_FOLDER_HOST = 3048
VIX_PROPERTY_JOB_RESULT_SHARED_FOLDER_FLAGS = 3049
VIX_PROPERTY_JOB_RESULT_PROCESS_ID = 3051
VIX_PROPERTY_JOB_RESULT_PROCESS_OWNER = 3052
VIX_PROPERTY_JOB_RESULT_PROCESS_COMMAND = 3053
VIX_PROPERTY_JOB_RESULT_FILE_FLAGS = 3054
VIX_PROPERTY_JOB_RESULT_PROCESS_START_TIME = 3055
VIX_PROPERTY_JOB_RESULT_VM_VARIABLE_STRING = 3056
VIX_PROPERTY_JOB_RESULT_PROCESS_BEING_DEBUGGED = 3057
VIX_PROPERTY_JOB_RESULT_SCREEN_IMAGE_SIZE = 3058
VIX_PROPERTY_JOB_RESULT_SCREEN_IMAGE_DATA = 3059
VIX_PROPERTY_JOB_RESULT_FILE_SIZE = 3061
VIX_PROPERTY_JOB_RESULT_FILE_MOD_TIME = 3062
VIX_PROPERTY_JOB_RESULT_EXTRA_ERROR_INFO = 3084
VIX_PROPERTY_FOUND_ITEM_LOCATION = 4010
VIX_PROPERTY_SNAPSHOT_DISPLAYNAME = 4200
VIX_PROPERTY_SNAPSHOT_DESCRIPTION = 4201
VIX_PROPERTY_SNAPSHOT_POWERSTATE = 4205
VIX_PROPERTY_SNAPSHOT_IS_REPLAYABLE = 4207
VIX_PROPERTY_GUEST_SHAREDFOLDERS_SHARES_PATH = 4525
VIX_PROPERTY_VM_ENCRYPTION_PASSWORD = 7001
VIX_EVENTTYPE_JOB_COMPLETED = 2
VIX_EVENTTYPE_JOB_PROGRESS = 3
VIX_EVENTTYPE_FIND_ITEM = 8
VIX_EVENTTYPE_CALLBACK_SIGNALLED = 2
VIX_FILE_ATTRIBUTES_DIRECTORY = 0x0001
VIX_FILE_ATTRIBUTES_SYMLINK = 0x0002
VIX_HOSTOPTION_USE_EVENT_PUMP = 0x0008
VIX_SERVICEPROVIDER_DEFAULT = 1
VIX_SERVICEPROVIDER_VMWARE_SERVER = 2
VIX_SERVICEPROVIDER_VMWARE_WORKSTATION = 3
VIX_SERVICEPROVIDER_VMWARE_PLAYER = 4
VIX_SERVICEPROVIDER_VMWARE_VI_SERVER = 10
VIX_API_VERSION = -1
VIX_FIND_RUNNING_VMS = 1
VIX_FIND_REGISTERED_VMS = 4
VIX_VMOPEN_NORMAL = 0x0
VIX_PUMPEVENTOPTION_NONE = 0
VIX_VMPOWEROP_NORMAL = 0
VIX_VMPOWEROP_FROM_GUEST = 0x0004
VIX_VMPOWEROP_SUPPRESS_SNAPSHOT_POWERON = 0x0080
VIX_VMPOWEROP_LAUNCH_GUI = 0x0200
VIX_VMPOWEROP_START_VM_PAUSED = 0x1000
VIX_VMDELETE_DISK_FILES = 0x0002
VIX_POWERSTATE_POWERING_OFF = 0x0001
VIX_POWERSTATE_POWERED_OFF = 0x0002
VIX_POWERSTATE_POWERING_ON = 0x0004
VIX_POWERSTATE_POWERED_ON = 0x0008
VIX_POWERSTATE_SUSPENDING = 0x0010
VIX_POWERSTATE_SUSPENDED = 0x0020
VIX_POWERSTATE_TOOLS_RUNNING = 0x0040
VIX_POWERSTATE_RESETTING = 0x0080
VIX_POWERSTATE_BLOCKED_ON_MSG = 0x0100
VIX_POWERSTATE_PAUSED = 0x0200
VIX_POWERSTATE_RESUMING = 0x0800
VIX_TOOLSSTATE_UNKNOWN = 0x0001
VIX_TOOLSSTATE_RUNNING = 0x0002
VIX_TOOLSSTATE_NOT_INSTALLED = 0x0004
VIX_VM_SUPPORT_SHARED_FOLDERS = 0x0001
VIX_VM_SUPPORT_MULTIPLE_SNAPSHOTS = 0x0002
VIX_VM_SUPPORT_TOOLS_INSTALL = 0x0004
VIX_VM_SUPPORT_HARDWARE_UPGRADE = 0x0008
VIX_LOGIN_IN_GUEST_REQUIRE_INTERACTIVE_ENVIRONMENT = 0x08
VIX_RUNPROGRAM_RETURN_IMMEDIATELY = 0x0001
VIX_RUNPROGRAM_ACTIVATE_WINDOW = 0x0002
VIX_VM_GUEST_VARIABLE = 1
VIX_VM_CONFIG_RUNTIME_ONLY = 2
VIX_GUEST_ENVIRONMENT_VARIABLE = 3
VIX_SNAPSHOT_REMOVE_CHILDREN = 0x0001
VIX_SNAPSHOT_INCLUDE_MEMORY = 0x0002
VIX_SHAREDFOLDER_WRITE_ACCESS = 0x04
VIX_CAPTURESCREENFORMAT_PNG = 0x01
VIX_CAPTURESCREENFORMAT_PNG_NOCOMPRESS = 0x02
VIX_CLONETYPE_FULL = 0
VIX_CLONETYPE_LINKED = 1
VIX_INSTALLTOOLS_MOUNT_TOOLS_INSTALLER = 0x00
VIX_INSTALLTOOLS_AUTO_UPGRADE = 0x01
VIX_INSTALLTOOLS_RETURN_IMMEDIATELY = 0x02

def setup_functions(vix):
    # functions
    vix.Vix_GetErrorText.restype = c_char_p
    vix.Vix_GetErrorText.argtypes = [VixError,c_char_p]
    vix.Vix_ReleaseHandle.restype = None
    vix.Vix_ReleaseHandle.argtypes = [VixHandle]
    vix.Vix_AddRefHandle.restype = None
    vix.Vix_AddRefHandle.argtypes = [VixHandle]
    vix.Vix_GetHandleType.restype = VixHandleType
    vix.Vix_GetHandleType.argtypes = [VixHandle]
    vix.Vix_GetProperties.restype = VixError
    # warning - vix.Vix_GetProperties takes variable argument list
    vix.Vix_GetProperties.argtypes = [VixHandle,VixPropertyID]
    vix.Vix_GetPropertyType.restype = VixError
    vix.Vix_GetPropertyType.argtypes = [VixHandle,VixPropertyID,POINTER(VixPropertyType)]
    vix.Vix_FreeBuffer.restype = None
    vix.Vix_FreeBuffer.argtypes = [c_void_p]
    vix.VixHost_Connect.restype = VixHandle
    vix.VixHost_Connect.argtypes = [c_int,VixServiceProvider,c_char_p,c_int,c_char_p,c_char_p,VixHostOptions,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixHost_Disconnect.restype = None
    vix.VixHost_Disconnect.argtypes = [VixHandle]
    vix.VixHost_RegisterVM.restype = VixHandle
    vix.VixHost_RegisterVM.argtypes = [VixHandle,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixHost_UnregisterVM.restype = VixHandle
    vix.VixHost_UnregisterVM.argtypes = [VixHandle,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixHost_FindItems.restype = VixHandle
    vix.VixHost_FindItems.argtypes = [VixHandle,VixFindItemType,VixHandle,c_int32,POINTER(VixEventProc),c_void_p]
    vix.VixHost_OpenVM.restype = VixHandle
    vix.VixHost_OpenVM.argtypes = [VixHandle,c_char_p,VixVMOpenOptions,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.Vix_PumpEvents.restype = None
    vix.Vix_PumpEvents.argtypes = [VixHandle,VixPumpEventsOptions]
    vix.VixPropertyList_AllocPropertyList.restype = VixError
    # warning - vix.VixPropertyList_AllocPropertyList takes variable argument list
    vix.VixPropertyList_AllocPropertyList.argtypes = [VixHandle,POINTER(VixHandle),c_int]
    vix.VixVM_Open.restype = VixHandle
    vix.VixVM_Open.argtypes = [VixHandle,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixVM_PowerOn.restype = VixHandle
    vix.VixVM_PowerOn.argtypes = [VixHandle,VixVMPowerOpOptions,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_PowerOff.restype = VixHandle
    vix.VixVM_PowerOff.argtypes = [VixHandle,VixVMPowerOpOptions,POINTER(VixEventProc),c_void_p]
    vix.VixVM_Reset.restype = VixHandle
    vix.VixVM_Reset.argtypes = [VixHandle,VixVMPowerOpOptions,POINTER(VixEventProc),c_void_p]
    vix.VixVM_Suspend.restype = VixHandle
    vix.VixVM_Suspend.argtypes = [VixHandle,VixVMPowerOpOptions,POINTER(VixEventProc),c_void_p]
    vix.VixVM_Pause.restype = VixHandle
    vix.VixVM_Pause.argtypes = [VixHandle,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_Unpause.restype = VixHandle
    vix.VixVM_Unpause.argtypes = [VixHandle,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_Delete.restype = VixHandle
    vix.VixVM_Delete.argtypes = [VixHandle,VixVMDeleteOptions,POINTER(VixEventProc),c_void_p]
    vix.VixVM_BeginRecording.restype = VixHandle
    vix.VixVM_BeginRecording.argtypes = [VixHandle,c_char_p,c_char_p,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_EndRecording.restype = VixHandle
    vix.VixVM_EndRecording.argtypes = [VixHandle,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_BeginReplay.restype = VixHandle
    vix.VixVM_BeginReplay.argtypes = [VixHandle,VixHandle,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_EndReplay.restype = VixHandle
    vix.VixVM_EndReplay.argtypes = [VixHandle,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_WaitForToolsInGuest.restype = VixHandle
    vix.VixVM_WaitForToolsInGuest.argtypes = [VixHandle,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_LoginInGuest.restype = VixHandle
    vix.VixVM_LoginInGuest.argtypes = [VixHandle,c_char_p,c_char_p,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_LogoutFromGuest.restype = VixHandle
    vix.VixVM_LogoutFromGuest.argtypes = [VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_RunProgramInGuest.restype = VixHandle
    vix.VixVM_RunProgramInGuest.argtypes = [VixHandle,c_char_p,c_char_p,VixRunProgramOptions,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_ListProcessesInGuest.restype = VixHandle
    vix.VixVM_ListProcessesInGuest.argtypes = [VixHandle,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_KillProcessInGuest.restype = VixHandle
    vix.VixVM_KillProcessInGuest.argtypes = [VixHandle,c_uint64,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_RunScriptInGuest.restype = VixHandle
    vix.VixVM_RunScriptInGuest.argtypes = [VixHandle,c_char_p,c_char_p,VixRunProgramOptions,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_OpenUrlInGuest.restype = VixHandle
    vix.VixVM_OpenUrlInGuest.argtypes = [VixHandle,c_char_p,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_CopyFileFromHostToGuest.restype = VixHandle
    vix.VixVM_CopyFileFromHostToGuest.argtypes = [VixHandle,c_char_p,c_char_p,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_CopyFileFromGuestToHost.restype = VixHandle
    vix.VixVM_CopyFileFromGuestToHost.argtypes = [VixHandle,c_char_p,c_char_p,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_DeleteFileInGuest.restype = VixHandle
    vix.VixVM_DeleteFileInGuest.argtypes = [VixHandle,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixVM_FileExistsInGuest.restype = VixHandle
    vix.VixVM_FileExistsInGuest.argtypes = [VixHandle,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixVM_RenameFileInGuest.restype = VixHandle
    vix.VixVM_RenameFileInGuest.argtypes = [VixHandle,c_char_p,c_char_p,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_CreateTempFileInGuest.restype = VixHandle
    vix.VixVM_CreateTempFileInGuest.argtypes = [VixHandle,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_GetFileInfoInGuest.restype = VixHandle
    vix.VixVM_GetFileInfoInGuest.argtypes = [VixHandle,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixVM_ListDirectoryInGuest.restype = VixHandle
    vix.VixVM_ListDirectoryInGuest.argtypes = [VixHandle,c_char_p,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_CreateDirectoryInGuest.restype = VixHandle
    vix.VixVM_CreateDirectoryInGuest.argtypes = [VixHandle,c_char_p,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_DeleteDirectoryInGuest.restype = VixHandle
    vix.VixVM_DeleteDirectoryInGuest.argtypes = [VixHandle,c_char_p,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_DirectoryExistsInGuest.restype = VixHandle
    vix.VixVM_DirectoryExistsInGuest.argtypes = [VixHandle,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixVM_ReadVariable.restype = VixHandle
    vix.VixVM_ReadVariable.argtypes = [VixHandle,c_int,c_char_p,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_WriteVariable.restype = VixHandle
    vix.VixVM_WriteVariable.argtypes = [VixHandle,c_int,c_char_p,c_char_p,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_GetNumRootSnapshots.restype = VixError
    vix.VixVM_GetNumRootSnapshots.argtypes = [VixHandle,POINTER(c_int)]
    vix.VixVM_GetRootSnapshot.restype = VixError
    vix.VixVM_GetRootSnapshot.argtypes = [VixHandle,c_int,POINTER(VixHandle)]
    vix.VixVM_GetCurrentSnapshot.restype = VixError
    vix.VixVM_GetCurrentSnapshot.argtypes = [VixHandle,POINTER(VixHandle)]
    vix.VixVM_GetNamedSnapshot.restype = VixError
    vix.VixVM_GetNamedSnapshot.argtypes = [VixHandle,c_char_p,POINTER(VixHandle)]
    vix.VixVM_RemoveSnapshot.restype = VixHandle
    vix.VixVM_RemoveSnapshot.argtypes = [VixHandle,VixHandle,VixRemoveSnapshotOptions,POINTER(VixEventProc),c_void_p]
    vix.VixVM_RevertToSnapshot.restype = VixHandle
    vix.VixVM_RevertToSnapshot.argtypes = [VixHandle,VixHandle,VixVMPowerOpOptions,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_CreateSnapshot.restype = VixHandle
    vix.VixVM_CreateSnapshot.argtypes = [VixHandle,c_char_p,c_char_p,VixCreateSnapshotOptions,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_EnableSharedFolders.restype = VixHandle
    vix.VixVM_EnableSharedFolders.argtypes = [VixHandle,c_byte,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_GetNumSharedFolders.restype = VixHandle
    vix.VixVM_GetNumSharedFolders.argtypes = [VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_GetSharedFolderState.restype = VixHandle
    vix.VixVM_GetSharedFolderState.argtypes = [VixHandle,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_SetSharedFolderState.restype = VixHandle
    vix.VixVM_SetSharedFolderState.argtypes = [VixHandle,c_char_p,c_char_p,VixMsgSharedFolderOptions,POINTER(VixEventProc),c_void_p]
    vix.VixVM_AddSharedFolder.restype = VixHandle
    vix.VixVM_AddSharedFolder.argtypes = [VixHandle,c_char_p,c_char_p,VixMsgSharedFolderOptions,POINTER(VixEventProc),c_void_p]
    vix.VixVM_RemoveSharedFolder.restype = VixHandle
    vix.VixVM_RemoveSharedFolder.argtypes = [VixHandle,c_char_p,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_CaptureScreenImage.restype = VixHandle
    vix.VixVM_CaptureScreenImage.argtypes = [VixHandle,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_Clone.restype = VixHandle
    vix.VixVM_Clone.argtypes = [VixHandle,VixHandle,VixCloneType,c_char_p,c_int,VixHandle,POINTER(VixEventProc),c_void_p]
    vix.VixVM_UpgradeVirtualHardware.restype = VixHandle
    vix.VixVM_UpgradeVirtualHardware.argtypes = [VixHandle,c_int,POINTER(VixEventProc),c_void_p]
    vix.VixVM_InstallTools.restype = VixHandle
    vix.VixVM_InstallTools.argtypes = [VixHandle,c_int,c_char_p,POINTER(VixEventProc),c_void_p]
    vix.VixJob_Wait.restype = VixError
    # warning - vix.VixJob_Wait takes variable argument list
    vix.VixJob_Wait.argtypes = [VixHandle,VixPropertyID]
    vix.VixJob_CheckCompletion.restype = VixError
    vix.VixJob_CheckCompletion.argtypes = [VixHandle,POINTER(c_byte)]
    vix.VixJob_GetError.restype = VixError
    vix.VixJob_GetError.argtypes = [VixHandle]
    vix.VixJob_GetNumProperties.restype = c_int
    vix.VixJob_GetNumProperties.argtypes = [VixHandle,c_int]
    vix.VixJob_GetNthProperties.restype = VixError
    # warning - vix.VixJob_GetNthProperties takes variable argument list
    vix.VixJob_GetNthProperties.argtypes = [VixHandle,c_int,c_int]
    vix.VixSnapshot_GetNumChildren.restype = VixError
    vix.VixSnapshot_GetNumChildren.argtypes = [VixHandle,POINTER(c_int)]
    vix.VixSnapshot_GetChild.restype = VixError
    vix.VixSnapshot_GetChild.argtypes = [VixHandle,c_int,POINTER(VixHandle)]
    vix.VixSnapshot_GetParent.restype = VixError
    vix.VixSnapshot_GetParent.argtypes = [VixHandle,POINTER(VixHandle)]

try:
    # if on Windows, may need to change following to use WinDLL instead of CDLL
    #vix = CDLL('vix.dll')
    vix = CDLL('/usr/lib/vmware-vix/libvixAllProducts.so')
except OSError:
    vix = None

if vix:
    setup_functions(vix)


