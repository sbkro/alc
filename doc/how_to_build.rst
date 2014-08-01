How to build
============

Requirement
-----------
No external libraries are needed to run the *'alc'*. But, to generate a
document and testing of this application, the following libraries
are required.

.. program-output:: cat ../requirements.txt

To install these libraries, execute follow command.::

    $ pip install -r requirements.txt

Build apps
----------
To build the application, call this command.::

    $ ./build_app.sh

Application files is as follows::

    ./alc.alfredworkflow

Build documents
---------------
To generate the document, call this command.::

    $ ./build_doc.sh

Document files is as follows::

    ./doc/_build/html/index.html

.. seealso::

    I'm using the *shpinx* as documentation builder.
    In detail sphinx, refer to follow Web sites.

    * http://sphinx-doc.org (English)
    * http://sphinx-users.jp (Japanese)

Testing
-------
To execute testing code, call this commands.::

    $ cd ./src/tests
    $ nosetests

.. seealso::

    I'm using the *nose* as a testing framework.
    In detail nose, refer to nose's Web site.

    * https://nose.readthedocs.org/en/latest/
