|badge_pipelines|_
|badge_coverage|_

.. |badge_pipelines| image:: https://gitlab.com/prometheuscomputing/rules-based-validator/badges/develop/pipeline.svg
.. _badge_pipelines: https://gitlab.com/prometheuscomputing/rules-based-validator
.. |badge_coverage| image::  https://gitlab.com/prometheuscomputing/rules-based-validator/badges/develop/coverage.svg
.. _badge_coverage: https://prometheuscomputing.gitlab.io/rules-based-validator/_static/coverage/index.html


``rbv`` will check whether a directory structure meets a list of rules
defined in a configuration ``rules.yml`` file.

Installation
------------

.. code:: bash

   $ git clone $GIT_URL
   $ cd rules-based-validator
   $ make install

Usage
-----

.. code:: bash

   $ rbv validate rules.yml
   $ rbv lint rules.yml

An example ``rules.yml``

.. code:: yaml

   - rulename: arbitraryrulename
     filters:
       path_list:
         - "Makefile"
         - "setup.py"
         - "rbv/cli.py"
     actions:
       exists: true

Filters and Actions
-------------------

Each rule is described by two different concepts:

    * Filters
        Select the files to which the rule will be applied.
    * Actions
        Run various checks on the files selected by the filters

Each rule is considered valid if all actions taken on the files selected
by the filters returned a 0 exit code (success).

Filters
~~~~~~~

+-----------------+------------------+-----------------------------+-----------+
| Name            | Usage            | Description                 |  Status   |
+=================+==================+=============================+===========+
|                 |.. code:: yaml    |                             |           |
|                 |                  | Find files by a             |           |
| path            | path: "*.json"   | single name or pattern.     |  Stable   |
|                 |                  |                             |           |
+-----------------+------------------+-----------------------------+-----------+
|                 |.. code:: yaml    |Find files from list         |           |
|                 |                  |of names or patterns.        |           |
| path_list       | path_list:       |                             |  Stable   |
|                 |   - "hello.txt"  |                             |           |
+-----------------+------------------+-----------------------------+-----------+
|                 |.. code:: yaml    |Find files from file with    |           |
|                 |                  |names or patterns,           |           |
| paths_from_file | paths_from_file: |one per line.                |  Beta     |
|                 | "paths.txt"      |                             |           |
+-----------------+------------------+-----------------------------+-----------+


N.B. Compatible pattern matching expressions: anything compatible with
``glob``

Actions
~~~~~~~

+-----------------+--------------------+-----------------------------+-----------+
| Name            | Usage              | Description                 |  Status   |
+=================+====================+=============================+===========+
|                 |.. code:: yaml      |                             |           |
|                 |                    |                             |           |
| exists          | path: "*.json"     | Selected files exist,       |  Stable   |
|                 |                    | (e.g. a minimum of 1 found) |           |
+-----------------+--------------------+-----------------------------+-----------+
|                 |.. code:: yaml      |                             |           |
|                 |                    | Find exactly n              |           |
| count           | path_list:         |  selected files.            |  Stable   |
|                 |   - "hello.txt"    |                             |           |
+-----------------+--------------------+-----------------------------+-----------+
|                 |.. code:: yaml      | For each selected file,     |           |
|                 |                    | check the existence of      |           |
| match           | match:             | another file                |  Stable   |
|                 | "{DIR_NAME}/o.txt" |                             |           |
+-----------------+--------------------+-----------------------------+-----------+


Substitutions
^^^^^^^^^^^^^

*N.B.* Only available in ``action.match``

In some rules, it may be necessary to use information about the filtered
files to make a determination on an action. The substitutions keys below
are available for use in the parameter of the ``match`` action.

For example, the following will check that every file matching
``predictions/*/predictions.csv`` has a corresponding ``JSON`` file with
the original directory name as its filename.

.. code:: yaml

   - rulename: predictions_file
     filters:
       path: "predictions/*/predictions.csv"
     actions:
       match: "pipelines/{DIR_NAME}.json"

Examples are based on the file path ``a/b/c.txt``

+----------------------+------------------------------------+---------------+
| Substitution keys    |   Description                      | Example value |
+======================+====================================+===============+
| ``{DIR_NAME}``       |  the directory name                | ``b``         |
+----------------------+------------------------------------+---------------+
| ``{DIR_PATH}``       |  the directory path                | ``a/b``       |
+----------------------+------------------------------------+---------------+
| ``{FILENAME_NOEXT}`` | the filename without the extension | ``c``         |
+----------------------+------------------------------------+---------------+
| ``{FILENAME}``       | the filename with the extension    | ``c.txt``     |
+----------------------+------------------------------------+---------------+
| ``{FILEPATH}``       | the file path                      | ``a/b/c.txt`` |
+----------------------+------------------------------------+---------------+
