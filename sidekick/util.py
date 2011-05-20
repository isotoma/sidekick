
import time, os, re
import fcntl
import array
import struct
import socket
import platform

SIOCGIFCONF = 0x8912
MAXBYTES = 8096

def interfaces():
    arch = platform.architecture()[0]

    if arch == '32bit':
        var1 = 32
        var2 = 32
    elif arch == '64bit':
        var1 = 16
        var2 = 40
    else:
        raise OSError("Unknown architecture: %s" % arch)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buffer = array.array('B', '\0' * MAXBYTES)

    outbytes = struct.unpack('iL', fcntl.ioctl(
        sock.fileno(),
        SIOCGIFCONF,
        struct.pack('iL', MAXBYTES, buffer.buffer_info()[0])
        ))[0]

    namestr = buffer.tostring()

    for i in xrange(0, outbytes, var2):
        iface = namestr[i:i+var1].split('\0', 1)[0]
        ip = socket.inet_ntoa(namestr[i+20:i+24])
        yield iface, ip


def register_builtin_keys():
    path = os.path.join(os.path.dirname(__file__), "resources", "sidekick_rsa")
    os.system("ssh-add %s" % path)

def tail(path):
    #FIXME: Track inode num so we can survive logrotate
    st_size = os.stat(path).st_size

    fp = open(path)
    fp.seek(st_size)

    while True:
        line = fp.readline()

        if line:
            yield line
        else:
            time.sleep(1)

def tail_vmware_dhcp():
    regex = re.compile("DHCPACK on (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) to (?P<mac>([0-9a-f]{2}\:){5}[0-9a-f]{2}) via ")
    for line in tail('/var/log/daemon.log'):
        m = regex.search(line)
        if not m:
            continue
        yield m.group('mac'), m.group('ip')


