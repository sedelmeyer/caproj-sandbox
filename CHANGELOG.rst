Changelog
=========

Future releases
---------------

.. todo::

    * Add data cleansing pipeline requirements into ``caproj.data`` module Mixin classes

      * Create ``caproj.data.CleanMixin`` class

        * Identify missing data
        * Remove records with no PID or no record date
        * Confirm no duplicate PID / datetime combos
        * Add change index column
        * Add record unique ID column
        * Fill missing project attribute fields based on prior or next earliest available info
        * Fill project budget and schedule values

    * Add missing data inspection and handling functionality to ``caproj.BaseData`` class via a new ``MissingMixin`` class

    * Add Makefile for triggering data cleansing pipeline

    * Add an ``IntervalMixin`` class for subsetting project change records based on desired year-interval


v0.0.4 (2020-07-24)
-------------------

* Add tox automated tests for ``py36``, ``py37``, ``py38``, ``docs``, ``linter``
* Add GitHub Actions workflow with CI test matrix
* Add ``caproj.data.BaseData`` class as interface for accessing all data operations
* Add ``caproj.data.base.BaseDataOps`` class for providing ``BaseData``'s core IO functionality
* Add ``caproj.data.clean.CleanMixin`` class for providing ``BaseData`` with required data cleansing functionality
* Rename project repo from ``nyc-capital-projects`` to ``caproj-sandbox`` to reflect experimental nature of this repo


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
