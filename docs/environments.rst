============
Environments
============

Sidekick supports instancing your projects in multiple environments, both to desktop virtualisation software and to cloud providers (via the apache libcloud project).

You can manage the environments via the sidekick env subcommand.

Defining Environments
=====================

You define environments with the 'sidekick env define' command. It takes 2 mandatory arguments. The first is a name you want to refer to the environment by. The second is the name of the backend. If the backend requires extra configuration you can pass it on the command line too, as shown here::

    sidekick env define NAME BACKEND key1=value key2=value key3=value


VMWare Workstation/Player
-------------------------

The VMWare Workstation and Player support depends on the VIX API. This may need to be installed seperately, especially in the case of VMWare player. Unfortunately, VMWare Fusion does not seem to support VIX. Currently it doesn't take any parameters, but it does need defining before it can be used::

    sidekick env define vmw vmware


VirtualBox
----------

The VirtualBox support currently targets the 4.0 API and is primarily developed on OSX. Currently it doesn't take any parameters.

The first time you run sidekick it will check for it and create a virtualbox environment automatically if possible. If you install
virtualbox later you will need to define the environment before it is available to your clusters::

    sidekick env define vb virtualbox


Brightbox
---------

Sidekick can deploy your project to Brightbox, a Leeds based cloud provider. To define a brightbox environment you need a client id and secret. Brightbox will provide these when you have signed up.

You create the environment through the command line::

    sidekick env define bb brightbox client_id=cli-1234 secret=secret


Listing Environments
====================

You can list your environments with::

    sidekick env list

Deleting Environments
=====================

If you decide to switch virtualisation technology or to a different cloud provider then you might want to remove old environments. You can do so with::

    sidekick env delete ENVIRONMENT

