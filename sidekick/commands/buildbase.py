
import os, platform, tempfile

from sidekick.command import Command


postboot = """\
#!/bin/sh

# Add an admin user
chroot $1 adduser --ingroup admin sidekick

# This is a workaround for KVM vm's and virtio.....
# cat > $1/etc/udev/rules.d/virtio.rules << HERE
# KERNEL=="vda*", SYMLINK+="sda%%n"
# HERE

# Install vmware tools...
chroot $1 apt-get install -y -q --no-install-recommends open-vm-tools

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

"""


class BuildBase(Command):

    """
    Build a base VM using the ubuntu-vm-builder tool
    """

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
            "standard^", "server^", "gpgv", "openssh-server", "sudo",
            ],
        }

    def setup_optparse(self, p):
        p.add_option("-h", "--hypervisor", action="store", default="vmw6")
        p.add_option("-s", "--suite", action="store", default="lucid")

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
        print >>f, self.postboot % {
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

        execute = "ubuntu-vm-builder %s %s -d%s %s" % (
            self.options.hypervisor,
            self.options.suite,
            self.args[0],
            " ".join(optstring))

        if os.getuid() != 0:
            execute = "sudo " + execute

        print execute
        os.system(execute)


