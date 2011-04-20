
import time, os

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
    for line in tail('/var/log/daemon.log'):
        """
        Apr 20 18:43:49 cocacola vmnet-dhcpd: DHCPREQUEST for 192.168.202.130 from 00:0c:29:70:43:66 via vmnet8
        Apr 20 18:43:49 cocacola vmnet-dhcpd: DHCPACK on 192.168.202.130 to 00:0c:29:70:43:66 via vmnet8
        """

