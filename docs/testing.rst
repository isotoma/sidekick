=======
Testing
=======

Sidekick features a test runner that allows you to test your configuration
on any of the supported backends.

To have sidekick discover any suitable tests in the current directory (and
its children) and run them on the default backend you can simply::

    $ sidekick test

If you want to run it on a specific backend you can do::

    $ sidekick test -e vbox

