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


class ErrorType(type):
    errors = {}

    def __new__(meta, class_name, bases, new_attrs):
        cls = type.__new__(meta, class_name, bases, new_attrs)

        if "code" in new_attrs:
            if new_attrs["code"] in meta.errors:
                raise KeyError("Error code '%d' is already registered" % new_attrs["code"])

            meta.errors[new_attrs["code"]] = cls

        return cls

    @staticmethod
    def get(error_code, *args, **kwargs):
        return ErrorType.errors[error_code](*args, **kwargs)


class Error(Exception):
    __metaclass__ = ErrorType


class FAIL(Error):
    code = 1

class OUT_OF_MEMORY(Error):
    code = 2

class INVALID_ARG(Error):
    code = 3

class FILE_NOT_FOUND(Error):
    code = 4

class OBJECT_IS_BUSY(Error):
    code = 5

class NOT_SUPPORTED(Error):
    code = 6

class FILE_ERROR(Error):
    code = 7

class DISK_FULL(Error):
    code = 8

class INCORRECT_FILE_TYPE(Error):
    code = 9

class CANCELLED(Error):
    code = 10

class FILE_READ_ONLY(Error):
    code = 11

class FILE_ALREADY_EXISTS(Error):
    code = 12

class FILE_ACCESS_ERROR(Error):
    code = 13

class REQUIRES_LARGE_FILES(Error):
    code = 14

class FILE_ALREADY_LOCKED(Error):
    code = 15

class VMDB(Error):
    code = 16

class NOT_SUPPORTED_ON_REMOTE_OBJECT(Error):
    code = 20

class FILE_TOO_BIG(Error):
    code = 21

class FILE_NAME_INVALID(Error):
    code = 22

class ALREADY_EXISTS(Error):
    code = 23

class BUFFER_TOOSMALL(Error):
    code = 24

class OBJECT_NOT_FOUND(Error):
    code = 25

class HOST_NOT_CONNECTED(Error):
    code = 26

class INVALID_UTF8_STRING(Error):
    code = 27

class OPERATION_ALREADY_IN_PROGRESS(Error):
    code = 31

class UNFINISHED_JOB(Error):
    code = 29

class NEED_KEY(Error):
    code = 30

class LICENSE(Error):
    code = 32

class VM_HOST_DISCONNECTED(Error):
    code = 34

class AUTHENTICATION_FAIL(Error):
    code = 35

class HOST_CONNECTION_LOST(Error):
    code = 36

class DUPLICATE_NAME(Error):
    code = 41

class INVALID_HANDLE(Error):
    code = 1000

class NOT_SUPPORTED_ON_HANDLE_TYPE(Error):
    code = 1001

class TOO_MANY_HANDLES(Error):
    code = 1002

class NOT_FOUND(Error):
    code = 2000

class TYPE_MISMATCH(Error):
    code = 2001

class INVALID_XML(Error):
    code = 2002

class TIMEOUT_WAITING_FOR_TOOLS(Error):
    code = 3000

class UNRECOGNIZED_COMMAND(Error):
    code = 3001

class OP_NOT_SUPPORTED_ON_GUEST(Error):
    code = 3003

class PROGRAM_NOT_STARTED(Error):
    code = 3004

class CANNOT_START_READ_ONLY_VM(Error):
    code = 3005

class VM_NOT_RUNNING(Error):
    code = 3006

class VM_IS_RUNNING(Error):
    code = 3007

class CANNOT_CONNECT_TO_VM(Error):
    code = 3008

class POWEROP_SCRIPTS_NOT_AVAILABLE(Error):
    code = 3009

class NO_GUEST_OS_INSTALLED(Error):
    code = 3010

class VM_INSUFFICIENT_HOST_MEMORY(Error):
    code = 3011

class SUSPEND_ERROR(Error):
    code = 3012

class VM_NOT_ENOUGH_CPUS(Error):
    code = 3013

class HOST_USER_PERMISSIONS(Error):
    code = 3014

class GUEST_USER_PERMISSIONS(Error):
    code = 3015

class TOOLS_NOT_RUNNING(Error):
    code = 3016

class GUEST_OPERATIONS_PROHIBITED(Error):
    code = 3017

class ANON_GUEST_OPERATIONS_PROHIBITED(Error):
    code = 3018

class ROOT_GUEST_OPERATIONS_PROHIBITED(Error):
    code = 3019

class MISSING_ANON_GUEST_ACCOUNT(Error):
    code = 3023

class CANNOT_AUTHENTICATE_WITH_GUEST(Error):
    code = 3024

class UNRECOGNIZED_COMMAND_IN_GUEST(Error):
    code = 3025

class CONSOLE_GUEST_OPERATIONS_PROHIBITED(Error):
    code = 3026

class MUST_BE_CONSOLE_USER(Error):
    code = 3027

class VMX_MSG_DIALOG_AND_NO_UI(Error):
    code = 3028

class NOT_ALLOWED_DURING_VM_RECORDING(Error):
    code = 3029

class NOT_ALLOWED_DURING_VM_REPLAY(Error):
    code = 3030

class OPERATION_NOT_ALLOWED_FOR_LOGIN_TYPE(Error):
    code = 3031

class LOGIN_TYPE_NOT_SUPPORTED(Error):
    code = 3032

class EMPTY_PASSWORD_NOT_ALLOWED_IN_GUEST(Error):
    code = 3033

class INTERACTIVE_SESSION_NOT_PRESENT(Error):
    code = 3034

class INTERACTIVE_SESSION_USER_MISMATCH(Error):
    code = 3035

class UNABLE_TO_REPLAY_VM(Error):
    code = 3039

class CANNOT_POWER_ON_VM(Error):
    code = 3041

class NO_DISPLAY_SERVER(Error):
    code = 3043

class VM_NOT_RECORDING(Error):
    code = 3044

class VM_NOT_REPLAYING(Error):
    code = 3045

class VM_NOT_FOUND(Error):
    code = 4000

class NOT_SUPPORTED_FOR_VM_VERSION(Error):
    code = 4001

class CANNOT_READ_VM_CONFIG(Error):
    code = 4002

class TEMPLATE_VM(Error):
    code = 4003

class VM_ALREADY_LOADED(Error):
    code = 4004

class VM_ALREADY_UP_TO_DATE(Error):
    code = 4006

class VM_UNSUPPORTED_GUEST(Error):
    code = 4011

class UNRECOGNIZED_PROPERTY(Error):
    code = 6000

class INVALID_PROPERTY_VALUE(Error):
    code = 6001

class READ_ONLY_PROPERTY(Error):
    code = 6002

class MISSING_REQUIRED_PROPERTY(Error):
    code = 6003

class INVALID_SERIALIZED_DATA(Error):
    code = 6004

class PROPERTY_TYPE_MISMATCH(Error):
    code = 6005

class BAD_VM_INDEX(Error):
    code = 8000

class INVALID_MESSAGE_HEADER(Error):
    code = 10000

class INVALID_MESSAGE_BODY(Error):
    code = 10001

class SNAPSHOT_INVAL(Error):
    code = 13000

class SNAPSHOT_DUMPER(Error):
    code = 13001

class SNAPSHOT_DISKLIB(Error):
    code = 13002

class SNAPSHOT_NOTFOUND(Error):
    code = 13003

class SNAPSHOT_EXISTS(Error):
    code = 13004

class SNAPSHOT_VERSION(Error):
    code = 13005

class SNAPSHOT_NOPERM(Error):
    code = 13006

class SNAPSHOT_CONFIG(Error):
    code = 13007

class SNAPSHOT_NOCHANGE(Error):
    code = 13008

class SNAPSHOT_CHECKPOINT(Error):
    code = 13009

class SNAPSHOT_LOCKED(Error):
    code = 13010

class SNAPSHOT_INCONSISTENT(Error):
    code = 13011

class SNAPSHOT_NAMETOOLONG(Error):
    code = 13012

class SNAPSHOT_VIXFILE(Error):
    code = 13013

class SNAPSHOT_DISKLOCKED(Error):
    code = 13014

class SNAPSHOT_DUPLICATEDDISK(Error):
    code = 13015

class SNAPSHOT_INDEPENDENTDISK(Error):
    code = 13016

class SNAPSHOT_NONUNIQUE_NAME(Error):
    code = 13017

class SNAPSHOT_MEMORY_ON_INDEPENDENT_DISK(Error):
    code = 13018

class SNAPSHOT_MAXSNAPSHOTS(Error):
    code = 13019

class SNAPSHOT_MIN_FREE_SPACE(Error):
    code = 13020

class SNAPSHOT_HIERARCHY_TOODEEP(Error):
    code = 13021

class HOST_DISK_INVALID_VALUE(Error):
    code = 14003

class HOST_DISK_SECTORSIZE(Error):
    code = 14004

class HOST_FILE_ERROR_EOF(Error):
    code = 14005

class HOST_NETBLKDEV_HANDSHAKE(Error):
    code = 14006

class HOST_SOCKET_CREATION_ERROR(Error):
    code = 14007

class HOST_SERVER_NOT_FOUND(Error):
    code = 14008

class HOST_NETWORK_CONN_REFUSED(Error):
    code = 14009

class HOST_TCP_SOCKET_ERROR(Error):
    code = 14010

class HOST_TCP_CONN_LOST(Error):
    code = 14011

class HOST_NBD_HASHFILE_VOLUME(Error):
    code = 14012

class HOST_NBD_HASHFILE_INIT(Error):
    code = 14013

class DISK_INVAL(Error):
    code = 16000

class DISK_NOINIT(Error):
    code = 16001

class DISK_NOIO(Error):
    code = 16002

class DISK_PARTIALCHAIN(Error):
    code = 16003

class DISK_NEEDSREPAIR(Error):
    code = 16006

class DISK_OUTOFRANGE(Error):
    code = 16007

class DISK_CID_MISMATCH(Error):
    code = 16008

class DISK_CANTSHRINK(Error):
    code = 16009

class DISK_PARTMISMATCH(Error):
    code = 16010

class DISK_UNSUPPORTEDDISKVERSION(Error):
    code = 16011

class DISK_OPENPARENT(Error):
    code = 16012

class DISK_NOTSUPPORTED(Error):
    code = 16013

class DISK_NEEDKEY(Error):
    code = 16014

class DISK_NOKEYOVERRIDE(Error):
    code = 16015

class DISK_NOTENCRYPTED(Error):
    code = 16016

class DISK_NOKEY(Error):
    code = 16017

class DISK_INVALIDPARTITIONTABLE(Error):
    code = 16018

class DISK_NOTNORMAL(Error):
    code = 16019

class DISK_NOTENCDESC(Error):
    code = 16020

class DISK_NEEDVMFS(Error):
    code = 16022

class DISK_RAWTOOBIG(Error):
    code = 16024

class DISK_TOOMANYOPENFILES(Error):
    code = 16027

class DISK_TOOMANYREDO(Error):
    code = 16028

class DISK_RAWTOOSMALL(Error):
    code = 16029

class DISK_INVALIDCHAIN(Error):
    code = 16030

class DISK_KEY_NOTFOUND(Error):
    code = 16052

class DISK_SUBSYSTEM_INIT_FAIL(Error):
    code = 16053

class DISK_INVALID_CONNECTION(Error):
    code = 16054

class DISK_ENCODING(Error):
    code = 16061

class DISK_CANTREPAIR(Error):
    code = 16062

class DISK_INVALIDDISK(Error):
    code = 16063

class DISK_NOLICENSE(Error):
    code = 16064

class DISK_NODEVICE(Error):
    code = 16065

class DISK_UNSUPPORTEDDEVICE(Error):
    code = 16066

class CRYPTO_UNKNOWN_ALGORITHM(Error):
    code = 17000

class CRYPTO_BAD_BUFFER_SIZE(Error):
    code = 17001

class CRYPTO_INVALID_OPERATION(Error):
    code = 17002

class CRYPTO_RANDOM_DEVICE(Error):
    code = 17003

class CRYPTO_NEED_PASSWORD(Error):
    code = 17004

class CRYPTO_BAD_PASSWORD(Error):
    code = 17005

class CRYPTO_NOT_IN_DICTIONARY(Error):
    code = 17006

class CRYPTO_NO_CRYPTO(Error):
    code = 17007

class CRYPTO_ERROR(Error):
    code = 17008

class CRYPTO_BAD_FORMAT(Error):
    code = 17009

class CRYPTO_LOCKED(Error):
    code = 17010

class CRYPTO_EMPTY(Error):
    code = 17011

class CRYPTO_KEYSAFE_LOCATOR(Error):
    code = 17012

class CANNOT_CONNECT_TO_HOST(Error):
    code = 18000

class NOT_FOR_REMOTE_HOST(Error):
    code = 18001

class INVALID_HOSTNAME_SPECIFICATION(Error):
    code = 18002

class SCREEN_CAPTURE_ERROR(Error):
    code = 19000

class SCREEN_CAPTURE_BAD_FORMAT(Error):
    code = 19001

class SCREEN_CAPTURE_COMPRESSION_FAIL(Error):
    code = 19002

class SCREEN_CAPTURE_LARGE_DATA(Error):
    code = 19003

class GUEST_VOLUMES_NOT_FROZEN(Error):
    code = 20000

class NOT_A_FILE(Error):
    code = 20001

class NOT_A_DIRECTORY(Error):
    code = 20002

class NO_SUCH_PROCESS(Error):
    code = 20003

class FILE_NAME_TOO_LONG(Error):
    code = 20004

class TOOLS_INSTALL_NO_IMAGE(Error):
    code = 21000

class TOOLS_INSTALL_IMAGE_INACCESIBLE(Error):
    code = 21001

class TOOLS_INSTALL_NO_DEVICE(Error):
    code = 21002

class TOOLS_INSTALL_DEVICE_NOT_CONNECTED(Error):
    code = 21003

class TOOLS_INSTALL_CANCELLED(Error):
    code = 21004

class TOOLS_INSTALL_INIT_FAILED(Error):
    code = 21005

class TOOLS_INSTALL_AUTO_NOT_SUPPORTED(Error):
    code = 21006

class TOOLS_INSTALL_GUEST_NOT_READY(Error):
    code = 21007

class TOOLS_INSTALL_SIG_CHECK_FAILED(Error):
    code = 21008

class TOOLS_INSTALL_ERROR(Error):
    code = 21009

class TOOLS_INSTALL_ALREADY_UP_TO_DATE(Error):
    code = 21010

class TOOLS_INSTALL_IN_PROGRESS(Error):
    code = 21011

class WRAPPER_WORKSTATION_NOT_INSTALLED(Error):
    code = 22001

class WRAPPER_VERSION_NOT_FOUND(Error):
    code = 22002

class WRAPPER_SERVICEPROVIDER_NOT_FOUND(Error):
    code = 22003

class WRAPPER_PLAYER_NOT_INSTALLED(Error):
    code = 22004

class WRAPPER_RUNTIME_NOT_INSTALLED(Error):
    code = 22005

class WRAPPER_MULTIPLE_SERVICEPROVIDERS(Error):
    code = 22006

class MNTAPI_MOUNTPT_NOT_FOUND(Error):
    code = 24000

class MNTAPI_MOUNTPT_IN_USE(Error):
    code = 24001

class MNTAPI_DISK_NOT_FOUND(Error):
    code = 24002

class MNTAPI_DISK_NOT_MOUNTED(Error):
    code = 24003

class MNTAPI_DISK_IS_MOUNTED(Error):
    code = 24004

class MNTAPI_DISK_NOT_SAFE(Error):
    code = 24005
class MNTAPI_DISK_CANT_OPEN(Error):
    code = 24006

class MNTAPI_CANT_READ_PARTS(Error):
    code = 24007

class MNTAPI_UMOUNT_APP_NOT_FOUND(Error):
    code = 24008

class MNTAPI_UMOUNT(Error):
    code = 24009

class MNTAPI_NO_MOUNTABLE_PARTITONS(Error):
    code = 24010

class MNTAPI_PARTITION_RANGE(Error):
    code = 24011

class MNTAPI_PERM(Error):
    code = 24012

class MNTAPI_DICT(Error):
    code = 24013

class MNTAPI_DICT_LOCKED(Error):
    code = 24014

class MNTAPI_OPEN_HANDLES(Error):
    code = 24015

class MNTAPI_CANT_MAKE_VAR_DIR(Error):
    code = 24016

class MNTAPI_NO_ROOT(Error):
    code = 24017

class MNTAPI_LOOP_FAILED(Error):
    code = 24018

class MNTAPI_DAEMON(Error):
    code = 24019

class MNTAPI_INTERNAL(Error):
    code = 24020

class MNTAPI_SYSTEM(Error):
    code = 24021

class MNTAPI_NO_CONNECTION_DETAILS(Error):
    code = 24022

class MNTAPI_INCOMPATIBLE_VERSION(Error):
    code = 24300

class MNTAPI_OS_ERROR(Error):
    code = 24301

class MNTAPI_DRIVE_LETTER_IN_USE(Error):
    code = 24302

class MNTAPI_DRIVE_LETTER_ALREADY_ASSIGNED(Error):
    code = 24303

class MNTAPI_VOLUME_NOT_MOUNTED(Error):
    code = 24304

class MNTAPI_VOLUME_ALREADY_MOUNTED(Error):
    code = 24305

class MNTAPI_FORMAT_FAILURE(Error):
    code = 24306

class MNTAPI_NO_DRIVER(Error):
    code = 24307

class MNTAPI_ALREADY_OPENED(Error):
    code = 24308

class MNTAPI_ITEM_NOT_FOUND(Error):
    code = 24309

class MNTAPI_UNSUPPROTED_BOOT_LOADER(Error):
    code = 24310

class MNTAPI_UNSUPPROTED_OS(Error):
    code = 24311

class MNTAPI_CODECONVERSION(Error):
    code = 24312

class MNTAPI_REGWRITE_ERROR(Error):
    code = 24313

class MNTAPI_UNSUPPORTED_FT_VOLUME(Error):
    code = 24314

class MNTAPI_PARTITION_NOT_FOUND(Error):
    code = 24315

class MNTAPI_PUTFILE_ERROR(Error):
    code = 24316

class MNTAPI_GETFILE_ERROR(Error):
    code = 24317

class MNTAPI_REG_NOT_OPENED(Error):
    code = 24318

class MNTAPI_REGDELKEY_ERROR(Error):
    code = 24319

class MNTAPI_CREATE_PARTITIONTABLE_ERROR(Error):
    code = 24320

class MNTAPI_OPEN_FAILURE(Error):
    code = 24321

class MNTAPI_VOLUME_NOT_WRITABLE(Error):
    code = 24322

class NET_HTTP_UNSUPPORTED_PROTOCOL(Error):
    code = 30001

class NET_HTTP_URL_MALFORMAT(Error):
    code = 30003

class NET_HTTP_COULDNT_RESOLVE_PROXY(Error):
    code = 30005

class NET_HTTP_COULDNT_RESOLVE_HOST(Error):
    code = 30006

class NET_HTTP_COULDNT_CONNECT(Error):
    code = 30007

class NET_HTTP_HTTP_RETURNED_ERROR(Error):
    code = 30022

class NET_HTTP_OPERATION_TIMEDOUT(Error):
    code = 30028

class NET_HTTP_SSL_CONNECT_ERROR(Error):
    code = 30035

class NET_HTTP_TOO_MANY_REDIRECTS(Error):
    code = 30047

class NET_HTTP_TRANSFER(Error):
    code = 30200

class NET_HTTP_SSL_SECURITY(Error):
    code = 30201

class NET_HTTP_GENERIC(Error):
    code = 30202


