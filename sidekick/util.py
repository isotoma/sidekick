
import time, os, re

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

def tail_daemon_log():
    regex = re.compile("DHCPACK on (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) to (?P<mac>([0-9a-f]{2}\:){5}[0-9a-f]{2}) via ")
    for line in tail('/var/log/daemon.log'):
        m = regex.search(line)
        if not m:
            continue
        yield m.group('mac'), m.group('ip')

for res in tail_daemon_log():
    print res