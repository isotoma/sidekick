==============
Other Commands
==============

buildbase
=========

Ubuntu users can use the buildbase command to build base images. It is based
on ubuntu-vm-builder.

ssh
===

The ssh command makes it easier to SSH in to nodes in your cluster. For a one
node cluster you might be able to get away with::

    sidekick ssh

Sidekick will determine the username, IP address and port of your node and
drop you into an SSH terminal.

nc
==

Sometimes it is handy to be able to nc to a node in your cluster with Sidekick
providing the connection details (ip address). An example of this is the ProxyCommand
directive in SSH. The following snippet in your SSH config will allow you to ssh to
a node without knowing its IP address or having to set up DNS::

    Host \*.sidekick
        ProxyCommand sidekick nc %h %p

Now any attempt to ssh, scp or use any tool using ssh (like libvirt or nautilus)
against web.mycluster.sidekick will work: Sidekick will determine the correct IP and
use it.

