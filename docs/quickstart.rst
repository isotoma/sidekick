==========
Quickstart
==========

In order to get the most out of Sidekick you need to know a little Yaybu. You
can find out more on the Yaybu site. Sidekick extends Yaybu a little and pushes
some information about your VM into the config that Yaybu deploys. This means
you know the IP etc in your configs. Lets write a simple Yaybu config that
sidekick can deploy. Let's call it web.yay::

    resources.append:
      - File:
          name: /tmp/${sidekick.primaryip}

Possibly the most useless configuration ever. But it shows that Yaybu is
getting the VM information from sidekick.

Currently deploying a new VM requires a Sidekick file. In the future simple
projects might not need this. The purpose of the Sidekick file is to be a
template to create Clusters from. A simple one would look like this::

    nodes:
      - name: web
        base: http://localhost/bases/lucid-amd64.tar.gz
        yaybu:
          recipe: web.yay

When you have a Sidekick file and some Yaybu to deploy into your VM you can
deploy it with::

    sidekick up

You can SSH in to your VM with the sidekick ssh helper::

    sidekick ssh

To deploy to the VM again use the deploy command::

    sidekick deploy

When you are done you can turn the VM off::

    sidekick down

And destroy it to free up space::

    sidekick destroy

Under the hood these commands are creating and using a default cluster that is
tied to the directory with the Sidekick file in. You can create a named cluster
instead, and thats how you can run a cluster on you local VMWare and on a remote
cloud provider.

For example, you might do something like this to set up an instance on
'acloudprovider'::

    sidekick env define mycloud -p acloudprovider clientid=myid key=d3adb33f
    sidekick define cloud_web -e mycloud
    sidekick up -c cloud_web

And then to setup and deploy to a local instance while the cloud instance is
still active::

    sidekick define local_web -e vmware
    sidekick up -c local_web

