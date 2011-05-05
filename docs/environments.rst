============
Environments
============

Sidekick supports instancing your projects in multiple environments, both to desktop virtualisation software and to cloud providers (via the apache libcloud project).

You can manage the environments via the sidekick env subcommand.

Defining Environments
=====================

VMWare Workstation/Player
-------------------------

The VMWare Workstation and Player support depends on the VIX API. This may need to be installed seperately, especially in the case of VMWare player. Currently it doesn't take any parameters, but it does need defining before it can be used::

    sidekick env define vmware backend=vmware


VirtualBox
----------

The VirtualBox support currently targets the 4.0 API and is primarily developed on OSX. Currently it doesn't take any parameters, but does need defining before it is available to your clusters::

    sidekick env define virtualbox backend=virtualbox


Brightbox
---------

Sidekick can deploy your project to Brightbox, a Leeds based cloud provider. To define a brightbox environment you need a client id and secret. Brightbox will provide these when you have signed up.

You create the environment through the command line::

    sidekick env define brightbox backend=brightbox client_id=cli-1234 secret=secret


Listing Environments
====================

You can list your environments with::

    sidekick env list

Deleting Environments
=====================

If you decide to switch virtualisation technology or to a different cloud provider then you might want to remove old environments. You can do so with::

    sidekick env delete ENVIRONMENT

