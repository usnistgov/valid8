*************************
YAML Specification
*************************

=====
Rules
=====

Rules are defined in YAML_ as a YAML list.

.. code-block:: yaml

    - [first rule content]
    - [second rule content]
    - [third rule content]

Each rule has 3 elements, expressed as key-value pairs in YAML:
  * a name : `rulename`
  * a set of filters under the key `filters`
  * a set of actions under the key `actions`

.. code-block:: yaml

    - rulename: first_rule
      filters:
        [filter set here]
      actions:
        [action set here]

.. _YAML: https://yaml.org/spec/1.2/spec.html

======================
Filters and Actions
======================

Any number of filters or actions can be listed under `filters` or `actions` as key-value pairs,
where the key is the filter (or action) function name and the value is the parameter sent to the filter or action.

.. code-block:: yaml

    - rulename: first_rule
      filters:
        existing_filter_function: parameter_for_filter
      actions:
        existing_action_function: parameter_for_action
        another_action_function:
          - parameter1_for_action
          - parameter2_for_action

c.f. the complete list of `available filters <readme.html#filters>`__ and `available actions <readme.html#actions>`__.

There are 3 types of parameters that can be passed to a filter or action.

--------------------------
Simple key-value parameter
--------------------------

.. code-block:: yaml

      actions:
        action_function: parameter_for_action

For example, the count action takes a single direct parameter: the number of files to expect. 

.. code-block:: yaml

      actions:
        count: 5

---------------
List parameters
---------------

.. code-block:: yaml

      filters:
        another_filter_function:
          - parameter1_for_filter
          - parameter2_for_filter

For example, the ``find`` filter can take a list of files (or patterns) to find:

.. code-block:: yaml

      filters:
        find:
          - find_this_file.txt
          - also_these_files.*


-----------------
Mapping parameter
-----------------


.. code-block:: yaml

      filters:
        another_filter_function:
          key_parameter: value
          another_key: another_value

For example, the ``find`` command can take a mapping parameter (but only for key ``file``):

.. code-block:: yaml

      filters:
        find:
          file: file_with_paths.txt

======================
Limitations
======================

Currently the `filters` and `actions` keys expect a mapping of filter or action functions.
It is therefore not possible to use the same filter or action twice.
