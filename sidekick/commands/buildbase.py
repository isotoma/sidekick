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


import os, platform, tempfile, glob

from sidekick.commands.base import Command

virtualbox = """
echo 1>&2 Installing virtualbox guest additions...
#chroot $1 apt-get install -y -q linux-headers-virtual virtualbox-ose-dkms virtualbox-ose-guest-dkms virtualbox-ose-guest-utils
"""

vmware = """
echo 1>&2 Installing vmware tools
chroot $1 apt-get install -y -q linux-headers-$(uname -r) open-vm-dkms open-vm-tools
"""

postboot = """\
#!/bin/sh

echo 1>&2 Adding PPA
cat > $1/etc/apt/sources.list.d/yaybu.list << EOF
deb http://ppa.launchpad.net/yaybu-team/yaybu-nightly/ubuntu %(suite)s main
deb-src http://ppa.launchpad.net/yaybu-team/yaybu-nightly/ubuntu %(suite)s main
EOF
chroot $1 apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A899DA54
chroot $1 apt-get update


echo 1>&2 Adding sidekick user

# Add an admin user
chroot $1 useradd -s /bin/bash -G admin sidekick

# Give the admin user an ssh folder
chroot $1 mkdir -p /home/sidekick/.ssh
chroot $1 chown sidekick /home/sidekick/.ssh
chroot $1 chmod 700 /home/sidekick/.ssh

echo 1>&2 Copying in authorized_keys

# With a specific SSH key
cp %(authorized_keys)s $1/home/sidekick/.ssh/authorized_keys
chroot $1 chown sidekick /home/sidekick/.ssh/authorized_keys

# This is a workaround for KVM vm's and virtio.....
# cat > $1/etc/udev/rules.d/virtio.rules << HERE
# KERNEL=="vda*", SYMLINK+="sda%%n"
# HERE

echo 1<&2 Configuring sudo

# Passwordless sudo
cat > $1/etc/sudoers << HERE
# /etc/sudoers
#
# This file MUST be edited with the 'visudo' command as root.
#
# See the man page for details on how to write a sudoers file.
#

Defaults        env_reset

# Host alias specification

# User alias specification

# Cmnd alias specification

# User privilege specification
root    ALL=(ALL) ALL

# Uncomment to allow members of group sudo to not need a password
# (Note that later entries override this, so you might need to move
# it further down)
# %%sudo ALL=NOPASSWD: ALL

# Members of the admin group may gain root privileges
%%admin ALL=(ALL) NOPASSWD: ALL
HERE

%(hypervisor)s

echo Installing yaybu
chroot $1 apt-get install -y -q rsyslog python-setuptools python-yaybu
"""


class BuildBase(Command):

    """ Build a base VM using the ubuntu-vm-builder tool """

    name = "buildbase"

    defaults = {
        "rootsize": 8192,
        "mem": 1024,
        "hostname": "sidekick",
        "variant": "minbase",
        "components": "main,universe,multiverse,restricted",
        "lang": "en_GB.UTF-8",
        "timezone": "Europe/London",
        "addpkg": [
            "standard^", "server^", "gpgv", "openssh-server", "sudo", "dhcp3-client",
            ],
        }

    def setup_optparse(self, p, a):
        p.add_option("-k", "--authorized-keys", action="store", default=os.path.expanduser("~/.ssh/id_rsa.pub"))
        p.add_option("-H", "--hypervisor", action="store", default="vmw6")
        p.add_option("-s", "--suite", action="store", default="lucid")

        a.append("destdir")

    def do(self):
        self.vmb_options = self.defaults.copy()

        self.set_arch()
        self.prepare_execscript()
        self.build()

    def set_arch(self):
        # 64 bit or 32 bit VM?
        if platform.machine() == "x86_64":
            self.vmb_options["arch"] = "amd64"
        else:
            self.vmb_options["arch"] = "i386"

    def prepare_execscript(self):
        f = tempfile.NamedTemporaryFile(delete=False, prefix="/var/tmp/")
        print >>f, postboot % {
            "suite": self.options.suite,
            "authorized_keys": self.options.authorized_keys,
            "hypervisor": {
                "vbox": virtualbox,
                "vmw6": vmware,
                }[self.options.hypervisor],
            }
        f.close()
        os.chmod(f.name, 0755)
        self.vmb_options['execscript'] = f.name

    def build(self):
        optstring = []
        for k, v in self.vmb_options.items():
            if type(v) == type([]):
                for i in v:
                    if i:
                        optstring.append("--%s=%s" % (k, i))
            else:
                if v:
                    optstring.append("--%s=%s" % (k, v))

        hypervisor = actual_hypervisor = self.options.hypervisor
        if actual_hypervisor == "vbox":
            hypervisor = "kvm"

        execute = "ubuntu-vm-builder %s %s -d%s %s" % (
            hypervisor,
            self.options.suite,
            self.args[0],
            " ".join(optstring))

        if os.getuid() != 0:
            execute = "sudo " + execute

        print execute
        os.system(execute)

        if actual_hypervisor == "vbox":
            src_path = glob.glob(os.path.join(self.args[0], "*.qcow2"))[0]
            bin_path = os.path.join(os.path.dirname(src_path), os.path.basename(self.args[0]) + ".bin")
            vdi_path = os.path.join(os.path.dirname(src_path), os.path.basename(self.args[0]) + ".vdi")

            commands = [
                "qemu-img convert %s %s" % (src_path, bin_path),
                "VBoxManage convertdd %s %s" % (bin_path, vdi_path),
                "VBoxManage modifyvdi %s compact" % vdi_path,
                ]

            for command in commands:
                print command
                os.system(command)

