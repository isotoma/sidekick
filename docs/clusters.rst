========
Clusters
========

A cluster is a group of virtual machines (nodes) needed to develop or demonstrate
your project. For a simple project you might only have one node, but you might want
to run your database and frontend on different VM's to better model production.
Sidekick natively supports managing as many nodes as needed to get this done and each
'instance' of your project is called a cluster.


Defining a new cluster
----------------------

A project will typically have a Sidekick file that describes the nodes in the cluster
and how to provision them (e.g. with Yaybu)::

    nodes:
      - name: web
        base: http://localhost/bases/lucid-amd64.tar.gz
        yaybu:
          recipe: web.yay

      - name: db
        base: http://localhost/bases/lucid-amd64.tar.gz
        yaybu:
          recipe: db.yay

This is only a template for a cluster, and we actually need to create a named instance of
it to make VM's. This lets us have a few instances of the same project running.

To actually turn this into a running cluster you can::

    sidekick define mycluster
    sidekick up


Deleting old clusters
---------------------

You can delete old clusters with the destroy command::

    sidekick destroy

If you want to destroy a specific cluster, you can do so by specifying the cluster option::

    sidekick destroy -c mycluter

