..
   Copyright © 2016 Stan Livitski

   This file is part of EPyColl. EPyColl is
   Licensed under the Apache License, Version 2.0 with modifications,
   (the "License"); you may not use this file except in compliance
   with the License. You may obtain a copy of the License at

   https://raw.githubusercontent.com/StanLivitski/EPyColl/master/LICENSE

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


=====================================
EPyColl - Enhanced Python collections 
=====================================

*EPyColl* is a set of structures and other tools that organize and
transform application data stored in memory. It provides features missing
from the standard collections_ library, such as immutable and reversible
mappings, and ordered collections.

About this repository
---------------------

This repository contains the source code of *EPyColl*.
Its top-level components are:

=========================    ===============================================
``mapping.py``               A module with structures and tools that
                             that help maintain mappings_ between objects.
``sets.py``                  A module with structures that implement the
                             `collections.Set`_ protocol to store sets
                             of unique items.
``LICENSE``                  Document that describes the project's licensing
                             terms.
``NOTICE``                   Summary of license terms that apply to
                             *EPyColl*. 
``README.rst``               This document.
=========================    ===============================================


Using EPyColl
-------------

Quick start
^^^^^^^^^^^

To start using *EPyColl* in your application, you should:

#. Comply with the toolkit's license terms. Please review the ``NOTICE``
   file at the root of this repository for licensing information.

#. Meet the `Dependencies`_ listed below in your runtime environment.

#. Add a copy of this directory to your ``PYTHONPATH`` or copy
   its contents to a package within your project. *If you place
   this code in a package, you'll have to qualify* ``import``
   *statements referring to it with the package name.*

Please refer to the modules' PyDoc comments for additional information
and usage examples.

Dependencies
^^^^^^^^^^^^

+-----------------------------------------------------------+---------------+
|  Name / Download URL                                      | Version       |
+===========================================================+===============+
| | Python                                                  | 3.0 or newer  |
| | https://www.python.org/downloads/ or an OS distribution |               |
+-----------------------------------------------------------+---------------+
| | ``python-runtime`` package                              | any available |
| | https://github.com/StanLivitski/python-runtime          |               |
+-----------------------------------------------------------+---------------+


.. _collections: https://docs.python.org/3.2/library/collections.html
.. _collections.Set: https://docs.python.org/3.2/library/collections.html#collections.Set
.. _mappings:
.. _collections.Mapping: https://docs.python.org/3.2/library/collections.html#collections.Mapping
