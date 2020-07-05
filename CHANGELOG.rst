Changelog
=========

Future releases
---------------

.. todo::

    * Recreate data cleansing pipeline with re-evaluated missing data handling
    * Recreate data sub-setting module

v0.1.0 (Future Release)
-------------------

* Add tox automated tests for ``py36``, ``py37``, ``py38``, ``docs``, ``linter``
* Add GitHub Actions CI test matrix

.. todo::

    * Add data cleansing pipeline as ``data`` submodules
    * Add basic EDA plotting functions to ``visualization`` submodules
    * Add ``datetime`` and other type-handling to ``BaseData``
    * Create ``data.clean`` mixin class
        * Identify missing data
        * Remove records with no PID or no record date
        * Confirm no duplicate PID / datetime combos
        * Add change index column
        * Add record unique ID column
        * Fill missing project attribute fields based on prior or next earliest available info
        * Fill project budget and schedule values


v0.0.3 (2020-06-09)
-------------------

* Add logging configuration and basic ``caproj.logger`` module functionality


v0.0.2 (2020-05-26)
-------------------

* fix setup.cfg to prevent travis-ci build fail


v0.0.1 (2020-05-25)
-------------------

* Generate intial site skeleton using ``gh-pages`` git branch
* Draft initial readme and introduction text
* Add custom project logo and favicon


v0.0.0 (2020-05-24)
-------------------

* Initial release with blank `Cookiecutter PyData`_ starter template

.. _Cookiecutter PyData: https://sedelmeyer.github.io/cc-pydata/
