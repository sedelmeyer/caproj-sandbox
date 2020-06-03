Changelog
=========

Future releases
---------------

.. todo::

    * Recreate data cleansing pipeline with re-evaluated missing data handling
    * Recreate data sub-setting module

v0.1.0 (XXXX-XX-XX)
-------------------

* Add data cleansing pipeline as ``data`` submodules
* Add basic EDA plotting functions to ``visualization`` submodules
* Add corresponding unit tests

.. todo::

    * Add ``datetime`` and other type-handling to ``BaseData``
    * Create ``data.clean`` mixin class
        * Identify missing data
        * Remove records with no PID or no record date
        * Confirm no duplicate PID / datetime combos
        * Add change index column
        * Add record unique ID column
        * Fill missing project attribute fields based on prior or next earliest available info
        * Fill project budget and schedule values


v0.0.1 (2020-05-25)
-------------------

* Generate intial site skeleton using ``gh-pages`` git branch
* Draft initial readme and introduction text
* Add custom project logo and favicon


v0.0.0 (2020-05-24)
-------------------

* Initial release with blank `Cookiecutter PyData`_ starter template

.. _Cookiecutter PyData: https://sedelmeyer.github.io/cc-pydata/
